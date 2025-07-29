import pytest
import asyncio
import time
import signal
from prefect_meemoo.prefect.deployment import (
    run_deployment_task,
    check_deployment_last_flow_run_failed,
    DeploymentModel,
    check_deployment_blocking,
    setup_sub_deployments_to_deployment_parameter,
    toggle_deployment_parameter_active,
    get_deployment_parameter
)
from prefect import flow, task, get_run_logger
from prefect.client.schemas.filters import FlowRunFilter
from prefect.deployments import Deployment, run_deployment
from prefect.client.orchestration import get_client
from prefect.states import StateType
from uuid import uuid1
from prefect.logging import disable_run_logger
from prefect.runtime import flow_run, deployment
import subprocess

@pytest.fixture(scope="module", autouse=True)
def setup_before_all_tests():
    print("\n[Setup] This runs once before any test in this file")
    proc_server = subprocess.Popen(['prefect', 'server', 'start'])
    time.sleep(10)

    proc = subprocess.Popen(['prefect', 'agent', 'start', '-q', 'default'])
    time.sleep(5)
    # Do your setup work here (e.g., start a service, prepare a DB, etc.)
    yield
    print("\n[Teardown] This runs after all tests in this file are done")
    proc_server.send_signal(signal.SIGINT)
    try:
        proc_server.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc_server.kill()
    proc.send_signal(signal.SIGINT)  
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()

@flow(name="test_check_deployment_failed_flows")
def failing_flow():
    raise Exception("Simulated failure for testing purposes.")

    # Create deployment

@pytest.mark.asyncio
async def test_check_deployment_failed_flows():
    """
    Test the check_deployment_failed_flows function.
    """
    
    deployment = await Deployment.build_from_flow(
        flow=failing_flow,
        name="failing-flow-deployment",
        work_queue_name="default",
    )
    await deployment.apply()
    print(f"Deployment created: {deployment}")
    # Trigger flow run
    flow_run = await run_deployment("test_check_deployment_failed_flows/failing-flow-deployment", timeout=0)
    print(f"Flow run triggered: {flow_run.id}")
    print(FlowRunFilter(deployment_id={'any_':[uuid1()]}, state={'type' : {'any_':["FAILED"]}}))

    # Wait for flow run to finish
    async with get_client() as client:
        for _ in range(1000):  # poll up to 30s
            run = await client.read_flow_run(flow_run.id)
            print(f"Current run state: {run.state.type}")
            if run.state.is_final():
                break
            await asyncio.sleep(1)

    with disable_run_logger():
        # Now check the result
        result = check_deployment_last_flow_run_failed("test_check_deployment_failed_flows/failing-flow-deployment")

    assert result is True

@flow(name="test_check_deployment_failed_flows_no_failures")
def successful_flow():
    return "This flow should succeed."

@pytest.mark.asyncio
async def test_check_deployment_failed_flows_no_failures():
    """
    Test the check_deployment_failed_flows function with a successful flow.
    """
    
    deployment = await Deployment.build_from_flow(
        flow=successful_flow,
        name="successful-flow-deployment",
        work_queue_name="default",
    )
    await deployment.apply()
    print(f"Deployment created: {deployment}")
    
    # Trigger flow run
    flow_run = await run_deployment("test_check_deployment_failed_flows_no_failures/successful-flow-deployment", timeout=0)
    print(f"Flow run triggered: {flow_run.id}")

    # Wait for flow run to finish
    async with get_client() as client:
        for _ in range(1000):
            run = await client.read_flow_run(flow_run.id)
            print(f"Current run state: {run.state.type}")
            if run.state.is_final():
                break
            await asyncio.sleep(1)
    with disable_run_logger():
        # Now check the result
        result = check_deployment_last_flow_run_failed("test_check_deployment_failed_flows_no_failures/successful-flow-deployment")
    assert result is False

@flow(name="test_deployment_blocking")
def blocking_flow():
    time.sleep(60)

@task(name="sleep_task")
def sleep_task(seconds: int):
    """
    Task that sleeps for a specified number of seconds.
    """
    time.sleep(seconds)
    return f"Slept for {seconds} seconds."

@flow(name="test_deployment_blocking_parent")
def blocking_parent_flow(
    blocking_deployment: DeploymentModel = DeploymentModel(
        name="test_deployment_blocking/blocking-flow-deployment",
        active=True,
        is_blocking=True,
        sub_deployments=[],
        full_sync=False,
    )
):
    """
    Flow that runs a blocking deployment.
    """
    logger = get_run_logger()
    dep_run = run_deployment_task.submit(blocking_deployment.name, as_subflow=False,)
    sleep = sleep_task.submit(30, wait_for=[dep_run])  # Simulate some work in the parent flow
    is_blocking = check_deployment_blocking.submit(blocking_deployment, wait_for=[dep_run, sleep]).result()
    logger.info(f"Blocking deployment check result: {is_blocking}")
    return is_blocking

@pytest.mark.asyncio
async def test_deployment_blocking():
    """
    Test the check_deployment_blocking function.
    """
    
    deployment_blocking = await Deployment.build_from_flow(
        flow=blocking_flow,
        name="blocking-flow-deployment",
        work_queue_name="default",
    )
    await deployment_blocking.apply()
    print(f"Blocking deployment created: {deployment_blocking}")

    result = blocking_parent_flow()
    assert result is True
    # deployment_partent = await Deployment.build_from_flow(
    #     flow=blocking_parent_flow,
    #     name="blocking-parent-flow-deployment",
    #     work_queue_name="default",
    # )
    # await deployment_partent.apply()
    # print(f"Blocking parent deployment created: {deployment_partent}")
    # # Trigger flow run
    # flow_run = await run_deployment("test_deployment_blocking_parent/blocking-parent-flow-deployment", timeout=0)
    
@flow(name="test_deployment_sub_deployment_1")
def sub_deployment_1(
    sub_deployment_2: DeploymentModel = DeploymentModel(
        name="test_deployment_sub_deployment_2/sub-deployment-2",
        active=True,
        is_blocking=False,
        sub_deployments=[],
        full_sync=False,
    )
):
    """
    Flow that runs a sub-deployment.
    """
    logger = get_run_logger()
    logger.info(f"Running sub-deployment 1 with sub-deployment 2: {sub_deployment_2.name}")

@flow(name="test_deployment_sub_deployment_2")
def sub_deployment_2():
    """
    Flow that runs a sub-deployment.
    """
    logger = get_run_logger()
    logger.info("Running sub-deployment 2")

@flow(name="test_deployment_sub_deployment_parent")
def sub_deployment_parent_flow(
    sub_deployment_1: DeploymentModel = DeploymentModel(
        name="test_deployment_sub_deployment_1/sub-deployment-1",
        active=True,
        is_blocking=False,
        sub_deployments=[],
        full_sync=False,
    )
):
    """
    Flow that runs a parent deployment with a sub-deployment.
    """
    logger = get_run_logger()
    logger.info(f"Running parent flow with sub-deployment 1: {sub_deployment_1.name}")
    setup_sub_deployments_to_deployment_parameter.submit(
        name=f"{flow_run.get_flow_name()}/{deployment.get_name()}",
        deployment_model=sub_deployment_1,
        deployment_model_parameter="sub_deployment_1"
    )
    sleep_task.submit(1000)  # Simulate some work in the parent flow

@pytest.mark.asyncio
def test_add_sub_depl():
    """
    Test the add_sub_deployments_to_deployment_param function.
    """
    
    deployment_1 = Deployment.build_from_flow(
        flow=sub_deployment_1,
        name="sub-deployment-1",
        work_queue_name="default",
        apply=True
    )
    deployment_1.apply()
    deployment_2 = Deployment.build_from_flow(
        flow=sub_deployment_2,
        name="sub-deployment-2",
        work_queue_name="default",
        apply=True
    )
    deployment_2.apply()
    
    deployment_parent = Deployment.build_from_flow(
        flow=sub_deployment_parent_flow,
        name="sub-deployment-parent",
        work_queue_name="default",
        apply=True,
    )
    
    run_deployment(
        "test_deployment_sub_deployment_parent/sub-deployment-parent",
    )
    
@flow(name="test_deployment_sub_deployment_parent_2")
def sub_deployment_parent_flow_2(
    sub_deployment_1: list[DeploymentModel] = [DeploymentModel(
        name="test_deployment_sub_deployment_1/sub-deployment-1",
        active=True,
        is_blocking=False,
        sub_deployments=[],
        full_sync=False,
    )]
):
    """
    Flow that runs a parent deployment with a sub-deployment.
    """
    logger = get_run_logger()
    setup_sub_deployments_to_deployment_parameter.submit(
        name=f"{flow_run.get_flow_name()}/{deployment.get_name()}",
        deployment_model=sub_deployment_1,
        deployment_model_parameter="sub_deployment_1"
    )
    sleep_task.submit(1000)  # Simulate some work in the parent flow

@pytest.mark.asyncio
def test_add_sub_depl_2():
    """
    Test the add_sub_deployments_to_deployment_param function with a list of sub-deployments.
    """
    
    deployment_1 = Deployment.build_from_flow(
        flow=sub_deployment_1,
        name="sub-deployment-1",
        work_queue_name="default",
        apply=True
    )
    
    deployment_parent = Deployment.build_from_flow(
        flow=sub_deployment_parent_flow_2,
        name="sub-deployment-parent-2",
        work_queue_name="default",
        apply=True,
    )
    
    run_deployment(
        "test_deployment_sub_deployment_parent_2/sub-deployment-parent-2",
    )
@flow(name="test_flow_with_deployment_parameter")
def flow_with_deployment_parameter(
    deployment_param = DeploymentModel(
        name="sth/sth-dep",
        active=True,
        is_blocking=False,
        sub_deployments=[],
        full_sync=False,
    )
):
    """
    Flow that uses a deployment parameter.
    """
    logger = get_run_logger()
    logger.info(f"Running flow with deployment parameter active: {deployment_param.active}")
    return

@flow(name="test_toggle_deployment_parameter_active")
def toggling_flow():
    """
    Flow that toggles the active state of a deployment parameter.
    """
    logger = get_run_logger()
    logger.info("Toggling deployment parameter active state.")
    active_state_1 = get_deployment_parameter.submit(
        name="test_flow_with_deployment_parameter/test-deployment-parameter",
        parameter_name="deployment_param",
    ).result()["active"]
    toggle_on = None
    if active_state_1 is not True:
        toggle_on = toggle_deployment_parameter_active.submit(
            name="test_flow_with_deployment_parameter/test-deployment-parameter",
            deployment_model_parameter="deployment_param",
            wait_for=[active_state_1]
        )
        sleeping_first = sleep_task.submit(5, wait_for=[toggle_on])  # Simulate some delay for the toggle to take effect
        active_state_1 = get_deployment_parameter.submit(
            name="test_flow_with_deployment_parameter/test-deployment-parameter",
            parameter_name="deployment_param",
            wait_for=[sleeping_first]
        ).result()["active"]
    assert active_state_1 is True, "Deployment parameter should be active after toggling."
    toggle = toggle_deployment_parameter_active.submit(
        name="test_flow_with_deployment_parameter/test-deployment-parameter",
        deployment_model_parameter="deployment_param",
        wait_for=[active_state_1, toggle_on]
    )
    sleeping = sleep_task.submit(5, wait_for=[toggle])  # Simulate some delay for the toggle to take effect
    active_state = get_deployment_parameter.submit(
        name="test_flow_with_deployment_parameter/test-deployment-parameter",
        parameter_name="deployment_param",
        wait_for=[sleeping]
    ).result()["active"]
    assert active_state is False, "Deployment parameter should be inactive after toggling."
    return

@pytest.mark.asyncio
async def test_toggle_deployment_parameter_active():
    """
    Test the toggle_deployment_parameter_active function.
    """
    deployment = await Deployment.build_from_flow(
        flow=flow_with_deployment_parameter,
        name="test-deployment-parameter",
        work_queue_name="default",
    )
    await deployment.apply()
    print(f"Deployment created: {deployment}")

    toggling_flow()
    
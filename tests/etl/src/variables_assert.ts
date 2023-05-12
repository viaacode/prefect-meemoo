import { Etl } from "@triplyetl/etl/generic";
import assert from 'assert';

export default async function () : Promise<Etl> {
    const app = new Etl()
    assert(process.env.SOMEVAR, "Test")
    assert(process.env.TEST, "Test")
    return app
}
import { Etl, Source, declarePrefix, forEach,  when, toRdf, Destination, fromJson } from "@triplyetl/etl/generic";
import {  triple, iri } from "@triplyetl/etl/ratt";
import {  a, sdo } from "@triplyetl/etl/vocab";

export default async function () : Promise<Etl> {
    const app = new Etl()
    const prefixes = {
        id: declarePrefix('https://data.hetarchief.be/id/')
    }

    console.log(`Execution dir: ${process.cwd()}`)

    app.use(
        fromJson(Source.file('../input/org-api-qas.json')),
        forEach('data.contentpartners',
            triple(iri(prefixes.id, 'id'), a, sdo.Person),
            
            when('label',
                triple(iri(prefixes.id, 'id'), sdo.name, 'label' )
            ),
        ),
        toRdf(Destination.file('../output/output.ttl')),
    )
    return app
}
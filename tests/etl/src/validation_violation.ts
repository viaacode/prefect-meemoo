import { Etl, Source, declarePrefix, forEach,  toRdf, Destination, fromJson } from "@triplyetl/etl/generic";
import {  triple, iri } from "@triplyetl/etl/ratt";
import { validate } from '@triplyetl/etl/shacl'
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
            triple(iri(prefixes.id, 'id'), a, sdo.Person)
        ),
        validate(Source.file('../input/schema.shacl.ttl')),
        toRdf(Destination.file('../output/output.ttl')),
    )
    return app
}
import { Etl, Source, declarePrefix, forEach, toRdf, Destination, fromJson } from "@triplyetl/etl/generic";
import {  triple, literal,  iri } from "@triplyetl/etl/ratt";
import { lang, rdfs } from "@triplyetl/etl/vocab";


export default async function () : Promise<Etl> {
    const app = new Etl()
    const prefixes = {
        id: declarePrefix('https://data.hetarchief.be/id/')
    }

    app.use(
        fromJson(Source.file('../input/org-api-qas.json')),
        forEach('data.contentpartners',
            triple(iri(prefixes.id, 'id'), rdfs.label, literal(process.env.TEST || "not found", lang.nl)),
        ),
        toRdf(Destination.file('../output/output-variables.ttl'))
    )
    return app
}
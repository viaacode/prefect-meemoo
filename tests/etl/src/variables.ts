import { Etl,  declarePrefix,  toRdf, Destination } from "@triplyetl/etl/generic";
import {  triple,  str,  iri } from "@triplyetl/etl/ratt";
import {  rdfs } from "@triplyetl/etl/vocab";

export default async function () : Promise<Etl> {
    const app = new Etl()
    const prefixes = {
        id: declarePrefix('https://data.hetarchief.be/id/')
    }

    app.use(
        triple(iri(prefixes.id, str('Jane')), rdfs.label, str(process.env.TEST)),
        toRdf(Destination.file('./static/output-variables.ttl'))
    )
    return app
}
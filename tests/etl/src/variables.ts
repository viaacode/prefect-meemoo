import { literal, a, forEach, fromJson, iri, logRecord, Ratt, toRdf, triple, when, str } from '@triplydb/ratt'
import { rdfs } from '@triplydb/ratt/lib/vocab'

export default async function () : Promise<Ratt> {
    const app = new Ratt()
    const prefixes = {
        id: Ratt.prefixer('https://data.hetarchief.be/id/')
    }

    app.use(
        triple(iri(prefixes.id, str('Jane')), rdfs.label, str(process.env.TEST)),
        toRdf(Ratt.Destination.file('./static/output-variables.ttl'))
    )
    return app
}
import { literal, a, forEach, fromJson, iri, logRecord, Ratt, toRdf, triple, when } from '@triplydb/ratt'
import { rdfs } from '@triplydb/ratt/lib/vocab'

export default async function () : Promise<Ratt> {
    const app = new Ratt()
    const prefixes = {
        id: Ratt.prefixer('https://data.hetarchief.be/id/')
    }

    app.use(
        fromJson(Ratt.Source.file('./static/org-api-qas.json')),
        forEach('data.contentpartners',
            triple(iri(prefixes.id, 'id'), rdfs.label, literal(process.env.TEST || "not found")),
        ),
        toRdf(Ratt.Destination.file('./static/output-variables.ttl'))
    )
    return app
}
import { a, forEach, fromJson, iri, logRecord, Ratt, toRdf, triple, when } from '@triplydb/ratt'
import { change } from '@triplydb/ratt/lib/middlewares/transforming/custom/change'
import { sdo } from '@triplydb/ratt/lib/vocab'

export default async function () : Promise<Ratt> {
    const app = new Ratt()
    const prefixes = {
        id: Ratt.prefixer('https://data.hetarchief.be/id/')
    }

    app.use(
        fromJson(Ratt.Source.file('./static/org-api-qas.json')),
        forEach('data.contentpartners',
            triple(iri(prefixes.id, 'id'), a, sdo.Person),
            
            when('label',
                triple(iri(prefixes.id, 'id'), sdo.name, 'label' )
            ),
        ),
        toRdf(Ratt.Destination.file('./static/output.ttl')),
    )
    return app
}
import EntityType from "../enums/entity-type.enum";

export function getEntityOfType(type, arr) {
    arr.push(fetch('http://corevision.ru/api/entities/list/' + type)
    .then((response) => response.json()))
}

export function getAllEntities(action) {
    let entities = []
    for (let item in EntityType)
    getEntityOfType(EntityType[item], entities)

    Promise.all(entities).then((data) => {
        action(data.flat(1))
    })
}
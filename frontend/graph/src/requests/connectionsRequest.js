

export function getConnectionOfType(number, arr) {
    arr.push(fetch('http://corevision.ru/api/type_connections/' + number)
    .then((response) => response.json().entity_connections))
}

export function getAllConnections(action) {
    let connections = []
    for (let i = 1; i < 18; i++)
    getConnectionOfType(i, connections)

    Promise.all(connections).then((data) => {
        action(data)
    })
}
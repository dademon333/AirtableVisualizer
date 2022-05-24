import * as d3 from 'd3'
import { useEffect } from 'react';
import IEntitiesAndConnectionsResponse from './libs/interfaces/response/entities-connections-response.interface';

function getRandomArbitrary(min: number, max: number) {
    return Math.random() * (max - min) + min;
}

interface INode {
    id: string;
    name: string;
    x: number;
    y: number;
}

interface ILink {
    source: INode;
    target: INode;
}

interface IGraph {
    nodes: INode[];
    links: ILink[];
}

const getGraph = (width: number, height: number, data: IEntitiesAndConnectionsResponse): IGraph =>  {
    const nodes = Object.entries(data.entities).map(entity => {
        const x = getRandomArbitrary(5, width - 5);
        const y = getRandomArbitrary(5, height - 5);
        const node: INode = {
            name: entity[1].name, x, y, id: entity[0]
        };

        return node;
    });
    const links: ILink[] = [];
    data.connections.map(connection => {
        connection.entities_connections.map(entityConnection => {
            const source = nodes.find(node => node.id == entityConnection.parent_id.toString());
            const target = nodes.find(node => node.id == entityConnection.child_id.toString());
            if (!source || !target) {return;}
            const link: ILink = {
                source, target
            };

            links.push(link);
        })
    });

    return { nodes, links };
}

const generateGraph = (data: IEntitiesAndConnectionsResponse) => {
    
    const svg = d3.select("svg");
    const width = Number(svg.attr("width"));
    const height = Number(svg.attr("height"));
    const graph = getGraph(width, height, data);
    var link = svg
    .append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter()
    .append("line")
    .attr("stroke-width", function(d) {
      return 3;
    })
    .attr("x1", function(d) { return d.source.x })
    .attr("y1", function(d) { return d.source.y })
    .attr("x2", function(d) { return d.target.x })
    .attr("y2", function(d) { return d.target.y });
  
  var node = svg
    .append("g")
    .attr("class", "nodes")
    .selectAll("circle")
    .data(graph.nodes)
    .enter()
    .append("circle")
    .attr("r", 5)
    .attr("transform", (d) => {
        return "translate(" + d.x + "," + d.y +")";
    })
    .attr("fill", function(d) {
      return "red";
    });
}



export default function Graph(data: IEntitiesAndConnectionsResponse): JSX.Element {

    useEffect(() => {
        generateGraph(data);
    }, []);


    return <svg width="5000" height="5000"></svg>;
}

export {};
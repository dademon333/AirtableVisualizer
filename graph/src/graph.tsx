import * as d3 from 'd3'
import { useEffect } from 'react';

function getRandomArbitrary(min: number, max: number) {
    return Math.random() * (max - min) + min;
}

interface INode {
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

const getGraph = (width: number, height: number): IGraph =>  {
    const names = [
        { name: "Alice" },
        { name: "Bob" },
        { name: "Chen" },
        { name: "Dawg" },
        { name: "Ethan" },
        { name: "George" },
        { name: "Frank" },
        { name: "Hanes" }
    ];

    const nodes = names.map(name => {
        const x = getRandomArbitrary(5, width - 5);
        const y = getRandomArbitrary(5, height - 5);
        const node: INode = {
            name: name.name, x, y
        };

        return node;
    });

    const links: ILink[] = [
        {
            source: nodes[0],
            target: nodes[1]
        },
        {
            source: nodes[2],
            target: nodes[1]
        },
        {
            source: nodes[3],
            target: nodes[2]
        },
        {
            source: nodes[7],
            target: nodes[6]
        },
        {
            source: nodes[7],
            target: nodes[5]
        },
        {
            source: nodes[3],
            target: nodes[4]
        }
    ]

    return { nodes,links };
}



const generateGraph = () => {
    
    const svg = d3.select("svg");
    const width = Number(svg.attr("width"));
    const height = Number(svg.attr("height"));
    const graph = getGraph(width, height);
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



export default function Graph(): JSX.Element {

    useEffect(() => {
        generateGraph();
    }, []);


    return <svg  width="960" height="600"></svg>;
}

export {};
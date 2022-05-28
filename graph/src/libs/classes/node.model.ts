import * as d3 from 'd3'
import INode from "../interfaces/graph/node.interface";
import { getEntityColor } from "../services/entity.serivce";

class NodeModel {

    //public selection: d3.Selection<SVGCircleElement, INode, SVGGElement, unknown>;
    public node: d3.Selection<SVGGElement, INode, SVGGElement, unknown>;

    constructor(svgElementName: string, nodes: INode[]) {
        const svg = d3.select(svgElementName);
        this.node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("g")
        .data(nodes)
        .enter()
        .append("g");

        this.appendCircle();

        this.appendText();
    }

    private appendCircle() {
        this.node
        .append("circle")
        .attr("r", (d) => 15 + d.connectedNodesCount / 5)
        .attr("fill", d => getEntityColor(d.type))
        .style("stroke-width", d => 0);
    }

    private appendText() {
        this.node
        .append("text")
        .attr("font-size", d => d.connectedNodesCount / 25 + 10)
        .attr("dx", 12)
        .attr("dy", "1em")
        .text(d => d.text);
    }
}

export default NodeModel;
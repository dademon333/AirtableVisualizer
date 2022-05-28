import * as d3 from 'd3'
import INode from "../interfaces/graph/node.interface";
import { getEntityColor } from "../services/entity.serivce";

class NodeModel {

    public selection: d3.Selection<SVGCircleElement, INode, SVGGElement, unknown>;
    public enter: d3.Selection<d3.EnterElement, INode, SVGGElement, unknown>;

    constructor(svgElementName: string, nodes: INode[]) {
        const svg = d3.select(svgElementName);
        this.enter = svg.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(nodes)
        .enter();

        this.selection = this.enter
        .append("circle")
        .attr("r", (d) => 10 + d.connectedNodesCount / 5)
        .attr("fill", d => getEntityColor(d.type))
        .style("stroke-width", d => 0);

        this.enter
        .append("text")
        .attr("dx", 12)
        .attr("dy", "1em")
        .text(function(d) { return "asdadjksaasdasd;sdasd" });
    }

    private appendCircle() {
        this.selection = this.enter
        .append("circle")
        .attr("r", (d) => 10 + d.connectedNodesCount / 5)
        .attr("fill", d => getEntityColor(d.type))
        .style("stroke-width", d => 0);
    }

    private appendText() {
        this.enter
        .append("text")
        .attr("dx", 12)
        .attr("dy", "1em")
        .text(function(d) { return "asdadjksaasdasd;sdasd" });
    }
}

export default NodeModel;
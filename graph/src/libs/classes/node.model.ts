import * as d3 from 'd3'
import INode from "../interfaces/graph/node.interface";
import { getEntityColor } from "../services/entity.serivce";

class NodeModel {

    //public container: d3.Selection<SVGGElement, INode, SVGGElement, unknown>;
    public node: d3.Selection<SVGGElement, INode, SVGGElement, unknown>;
    public circle: d3.Selection<SVGCircleElement, INode, SVGGElement, unknown>;
    public text: d3.Selection<SVGTextElement, INode, SVGGElement, unknown>;

    constructor(svgElementName: string, nodes: INode[]) {
        const svg = d3.select<SVGElement, any>(svgElementName);
        this.node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("g")
        .data(nodes)
        .enter()
        .append("g");

        this.circle = this.appendCircle();

        this.text = this.appendText();
    }

    private appendCircle(): d3.Selection<SVGCircleElement, INode, SVGGElement, unknown> {
        return this.node
        .append("circle")
        .on('mouseover', e => {
            const target = e.target;
            const id = target.__data__.id;
            this.node.filter(el => el.id !== id).attr('opacity', 0);
        })
        .on('mouseleave', e => {
            const target = e.target;
            console.log(target.__data__);
            this.node.attr('opacity', 1);
        })
        .attr("r", (d) => 15 + d.connectedNodesCount / 5)
        .attr("fill", d => getEntityColor(d.type))
        .style("stroke-width", d => 0);
    }

    private appendText(): d3.Selection<SVGTextElement, INode, SVGGElement, unknown> {
        return this.node
        .append("text")
        .attr("font-size", d => d.connectedNodesCount / 25 + 10)
        .attr("dx", 20)
        .attr("dy", "0.5em")
        .text(d => d.text);
    }
}

export default NodeModel;
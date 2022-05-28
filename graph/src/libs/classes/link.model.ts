import * as d3 from 'd3'
import ILink from "../interfaces/graph/nodes-link.interface";

class LinkModel {

    public selection: d3.Selection<SVGLineElement, ILink, SVGGElement, unknown>;
    private _svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>;

    constructor(svgElementName: string, links: ILink[]) {
        this._svg = d3.select(svgElementName);
        this.addArrow();

        this.selection = this._svg
        .append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(links)
        .enter()
        .append("line")
        .attr("stroke-width", d => 0.5)
        .attr("marker-start", "url(#end)");
    }

    private addArrow(): void {
        this._svg.append("svg:defs").selectAll("marker")
        .data(["end"])
        .enter().append("svg:marker")
        .attr("id", String)
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 42)
        .attr("refY", 0.5)
        .attr("markerWidth", 5)
        .attr("markerHeight", 5)
        .attr("orient", "auto")
        .append("svg:path")
        .attr("d", "M0,-5L10,0L0,5");
    }
}

export default LinkModel;
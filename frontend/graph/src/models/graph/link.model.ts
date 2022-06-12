import * as d3 from 'd3'
import SetType from '../../enums/set-type.enum';
import ILink from '../../interfaces/graph/nodes-link.interface';
import { IFilterState } from '../../redux/slices/filter.slice';
import store from '../../redux/store';
import { getEntityColor } from '../../services/entity.serivce';

class LinkModel {

    public selection: d3.Selection<SVGLineElement, ILink, SVGGElement, unknown>;
    private _svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>;

    constructor(svgElementName: string, links: ILink[]) {
        this._svg = d3.select(svgElementName);
        this.addArrow();

        this._svg.select('.links').remove();

        this.selection = this._svg
        .append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(links)
        .enter()
        .append("line")
        .attr("stroke-width", d => 0.5)
        .attr('opacity', 0)
        .attr("stroke", d => getEntityColor(d.source.type))
        .attr("marker-end", d => 15 + d.target.radius / 5);

        store.subscribe(() => {
            const state = store.getState();
            state.filters.components.setType === SetType.Union || state.filters.components.entities.length == 1 ? this.handleUnionSetType(state): this.handleIntersectionSetType(state);
        });
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

    private handleUnionSetType(state: {filters: IFilterState}) {
        const entitesToShow = store.getState().filters.components.entities;

        if (entitesToShow.length === 0) {
            this.selection.attr('opacity', 0);
            return;
        }

        this.selection.filter(el => !entitesToShow.includes(el.target.id)).attr('opacity', 0);
        this.selection.filter(el => entitesToShow.includes(el.target.id) || entitesToShow.includes(el.source.id)).attr('opacity', 1);
    }

    private handleIntersectionSetType(state: {filters: IFilterState}) {
        const entitesToShow = store.getState().filters.components.entities;

        if (entitesToShow.length === 0) {
            this.selection.attr('opacity', 0);
            return;
        }

        this.selection.attr('opacity', 0);
        this.selection.filter(el => {
            return entitesToShow.includes(el.source.id) && entitesToShow.includes(el.target.id)
            || (entitesToShow.includes(el.source.id) || entitesToShow.includes(el.target.id) )
            && 
            (el.source.connectedNodes.filter(node => entitesToShow.includes(node.id)).length >= entitesToShow.length
            || el.target.connectedNodes.filter(node => entitesToShow.includes(node.id)).length >= entitesToShow.length);
        }).attr('opacity', 1);
    }
}

export default LinkModel;
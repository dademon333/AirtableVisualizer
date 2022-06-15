import * as d3 from 'd3'
import SetType from '../../enums/set-type.enum';
import INode from '../../interfaces/graph/node.interface';
import ILink from '../../interfaces/graph/nodes-link.interface';
import { IFilterState } from '../../redux/slices/filter.slice';
import store from '../../redux/store';
import { getAllEntityTypes, getEntityColor } from '../../services/entity.serivce';

class LinkModel {

    public selection: d3.Selection<SVGLineElement, ILink, SVGGElement, unknown>;
    private _svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>;

    constructor(svgElementName: string, links: ILink[]) {
        this._svg = d3.select(svgElementName);
        this.addArrows();

        this._svg.select('.links').remove();

        this.selection = this._svg
        .append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(links)
        .enter()
        .append("line")
        .attr("refX", 250)
        .attr("refY", 250)
        .attr("stroke-width", d => 1)
        .attr('opacity', 0)
        .attr("stroke", d => getEntityColor(d.source.type))
        .attr('marker-end', (d) => `url(#arrow-${d.source.type})`)

        store.subscribe(() => {
            const state = store.getState();
            state.filters.components.setType === SetType.Union || state.filters.components.entities.length == 1 ? this.handleUnionSetType(state): this.handleIntersectionSetType(state);
        });
    }

    private addArrows(): void {
        const defs = this._svg.append('defs');
        getAllEntityTypes().forEach(el => {
            const marker = defs
            .append('marker')
            .attr('id', 'arrow' + `-${el}`)
            .attr('viewBox', [0, 0, 10, 10])
            .attr('refX', 17)
            .attr('refY', 5)
            .attr('markerWidth', 25)
            .attr('markerHeight', 50)
            .attr('orient', 'auto');

            marker
            .append('line')
            .attr('x1', 0)
            .attr('y1', 0)
            .attr('x2', 10)
            .attr('y2', 5)
            .attr('stroke', getEntityColor(el));

            marker
            .append('line')
            .attr('x1', 0)
            .attr('y1', 10)
            .attr('x2', 10)
            .attr('y2', 5)
            .attr('stroke', getEntityColor(el));
        });

    }

    private handleUnionSetType(state: {filters: IFilterState}) {
        const entitesToShow = store.getState().filters.components.entities;

        if (entitesToShow.length === 0) {
            this.selection.attr('opacity', 0);
            return;
        }

        this.selection.filter(el => !entitesToShow.includes(el.target.id)).attr('opacity', 0);
        this.selection.filter(el => entitesToShow.includes(el.source.id)).attr('opacity', 1);
    }

    private handleIntersectionSetType(state: {filters: IFilterState}) {
        const entitesToShow = store.getState().filters.components.entities;

        if (entitesToShow.length === 0) {
            this.selection.attr('opacity', 0);
            return;
        }

        const visibleNodes: INode[] = [];

        this.selection.each(d => {
            if (entitesToShow.some(el => el === d.source.id)) {
                visibleNodes.push(d.source);
                return;
            }

            if (entitesToShow.some(el => el === d.target.id)) {
                visibleNodes.push(d.target);
                return;
            }
        });

        this.selection.attr('opacity', 0);
        this.selection.filter(el => {
            //if (entitesToShow.some(id => id === el.source.id)) {
            //    return true;
            //}

            if (visibleNodes.every(visibleNode => visibleNode.children.some(cn => cn.id === el.target.id))) {
                return true;
            }

            return false;

        }).attr('opacity', 1);
    }
}

export default LinkModel;
import { Graph } from "react-d3-graph";

const GraphComponent = ({id, data, config}) => {
  return (
        <Graph
            id={id}
            data={data}
            config={config}
            // onClickNode={onClickNode}
            // onClickLink={onClickLink}
            // onClickGraph={onClickGraph}
        />
  )
}

export default GraphComponent

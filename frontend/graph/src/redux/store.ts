import { configureStore } from '@reduxjs/toolkit'
import entityConnectionSlice from './slices/entity-connection.slice'
import filterSlice from './slices/filter.slice'
import graphSlice from './slices/graph.slice'

export default configureStore({
  reducer: {
    entitiesConnections: entityConnectionSlice,
    filters: filterSlice,
    graph: graphSlice
  },
})
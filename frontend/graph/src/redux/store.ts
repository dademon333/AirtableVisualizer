import { configureStore } from '@reduxjs/toolkit'
import entityConnectionSlice from './slices/entity-connection.slice'
import filterSlice from './slices/filter.slice'

export default configureStore({
  reducer: {
    entitiesConnections: entityConnectionSlice,
    filters: filterSlice,
  },
})
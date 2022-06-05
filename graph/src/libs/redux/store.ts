import { configureStore } from '@reduxjs/toolkit'
import entityConnectionSlice from './slices/entity-connection.slice'

export default configureStore({
  reducer: {
    entitiesConnections: entityConnectionSlice
  },
})
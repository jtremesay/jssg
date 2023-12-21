import { Size } from "./widgets/base/size"

export const ITEM_SIZE = new Size(160, 135)
export const GRID_SIZE = new Size(6, 6)
export const CANVAS_SIZE = new Size(ITEM_SIZE.width * GRID_SIZE.width, ITEM_SIZE.height * GRID_SIZE.height)
export const TITLE_HEIGHT: number = 20

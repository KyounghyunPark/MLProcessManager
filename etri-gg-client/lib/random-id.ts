import { v4 as uuidv4 } from "uuid"
export const randomId = function(length = 16) {
  return Math.random().toString(36).substring(2, length+2);
  // return uuidv4()
};
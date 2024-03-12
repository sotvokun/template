export type TypeSafeUnionToIntersection<T, U extends T>
  = (U extends any ? (k: U) => void : never) extends ((k: infer I) => void) ? (I extends T ? I : never) : never;

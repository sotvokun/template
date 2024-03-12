import { Hono } from 'hono';
import type { Env, Schema } from 'hono'
import { BlankSchema, MiddlewareHandler } from 'hono/types'

import { TypeSafeUnionToIntersection } from './type.js'


export type ExtractMiddlewareHandlerEnv<T>
  = T extends MiddlewareHandler<infer E, any, any> ? E : never;

export type MergeEnv<T extends Env>
  = TypeSafeUnionToIntersection<Env, T>;

export type RouterSetup<
  E extends Env,
  S extends Schema,
  BasePath extends string,
> = (router: Hono<E, S, BasePath>) => void;


/**
  * Create a group of routes.
  */
export function createRouter<
  E extends Env = Env,
  S extends Schema = BlankSchema,
  BasePath extends string = string,
>(
  path: BasePath,
  setup: RouterSetup<MergeEnv<E>, S, BasePath>,
): Hono<MergeEnv<E>, S, BasePath>;


/**
  * Create a group of routes with middlewares.
  *
  * @note
  *    If you passed an empty array to `middlewares`, it will works like `createRouter/2`
  *
  * @note
  *    If you passed a type value into `E`, the type inferring will fallback to default.
  *    That means, the type inferring may not be accurate, `any` could be inferred.
  *    To resolve this, you should pass the type value by middleware way.
  */
export function createRouter<
  E extends Env = Env,
  S extends Schema = BlankSchema,
  BasePath extends string = string,
  M extends MiddlewareHandler[] = MiddlewareHandler[],
  ME extends Env = MergeEnv<E | ExtractMiddlewareHandlerEnv<M[number]>>,
>(
  path: BasePath,
  middlewares: M,
  setup: RouterSetup<ME, S, BasePath>,
): Hono<ME, S, BasePath>;


export function createRouter<
  E extends Env = Env,
  S extends Schema = BlankSchema,
  BasePath extends string = string,
  M extends MiddlewareHandler[] = MiddlewareHandler[],
  ME extends Env = MergeEnv<E | ExtractMiddlewareHandlerEnv<M[number]>>,
>(
  path: BasePath,
  middlewares: M | RouterSetup<MergeEnv<E>, S, BasePath>,
  setup?: RouterSetup<ME, S, BasePath>,
) {
  if (typeof middlewares === 'function') {
    const router = new Hono<MergeEnv<E>, S>().basePath(path);
    middlewares(router);
    return router;
  }
  const router = new Hono<ME, S>().basePath(path);
  router.use(...middlewares);
  if (setup) {
    setup(router);
  }
  return router;
}


/**
 * Get the base path of the router.
 *
 * @note This function hacked the private property of the router.
 */
export function getBasePath(router: Hono, extract?: boolean) {
  // @ts-expect-error
  const basePath = router._basePath;
  if (extract) {
    router.basePath('/')
  }
  return basePath
}

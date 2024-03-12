import { Env, Schema, Hono } from 'hono'
import { BlankSchema, MiddlewareHandler } from 'hono/types'
import { join } from 'node:path'
import fg from 'fast-glob'

import {
  ExtractMiddlewareHandlerEnv,
  MergeEnv,
  RouterSetup,
} from '@/utils/router.js'


// region: File based router
/**
 * Create a file based router
 */
export function createFileRouter<
  E extends Env = Env,
  S extends Schema = BlankSchema,
  BasePath extends string = '/',
  Setup extends RouterSetup<E, S, BasePath> = RouterSetup<E, S, BasePath>,
>(handler: Setup): {
  handler: Setup,
  middlewares: [],
}

/**
 * Create a file based router with middlewares
 */
export function createFileRouter<
  E extends Env = Env,
  S extends Schema = BlankSchema,
  BasePath extends string = '/',
  M extends MiddlewareHandler[] = MiddlewareHandler[],
  ME extends Env = MergeEnv<E | ExtractMiddlewareHandlerEnv<M[number]>>,
  Setup extends RouterSetup<ME, S, BasePath> = RouterSetup<ME, S, BasePath>,
>(
  middlewares: M,
  handler: Setup,
): {
  handler: Setup,
  middlewares: M,
}

export function createFileRouter<
  E extends Env = Env,
  S extends Schema = BlankSchema,
  BasePath extends string = '/',
  M extends MiddlewareHandler[] = MiddlewareHandler[],
  ME extends Env = MergeEnv<E | ExtractMiddlewareHandlerEnv<M[number]>>,
  Setup extends RouterSetup<ME, S, BasePath> = RouterSetup<ME, S, BasePath>,
>(
  middlewares: M | RouterSetup<E, S, BasePath>,
  handler?: Setup,
) {
  if (typeof middlewares === 'function') {
    return {
      handler: middlewares,
      middlewares: [],
    }
  } else {
    return {
      handler: handler!,
      middlewares,
    }
  }
}
// endregion: File based router


// region: Apply file routers

interface ApplyFileRoutersOptions extends fg.Options {
  /** The pattern for glob files */
  pattern: string[]
  dryRun?: boolean
  debug?: boolean
}

export async function applyFileRouters(app: Hono, options: ApplyFileRoutersOptions) {
  const FILE_EXT = /\.(ts|js|tsx|jsx)$/
  const INDEX_REGEX = /^index\.(?:ts|js|tsx|jsx)$/

  const files = fg.sync(options.pattern, options)
  const routes = files.map((filePath) => {
    const pathParts = filePath.split('/')
    const isIndex = INDEX_REGEX.test(pathParts[pathParts.length - 1])
    const isRootIndex = isIndex && pathParts.length === 1
    const urlPath = isRootIndex ? '/' : (
      isIndex
        ? `/${pathParts.slice(0, -1).join('/')}`
        : `/${pathParts.join('/').replace(FILE_EXT, '')}`)
    const level = isRootIndex ? 0 : (isIndex ? pathParts.length - 1 : pathParts.length)
    return {
      file: filePath,
      path: urlPath,
      level,
    }
  }).sort((a, b) => a.level - b.level)

  if (options.debug) {
    console.log(routes)
  }
  if (options.dryRun) {
    return app
  }

  for (let i = 0; i < routes.length; i++) {
    const route = routes[i]
    const path = join(options.cwd ? options.cwd : '', route.file)
    const { handler, middlewares } = (
      (await import(path.replace(FILE_EXT, '.js'))).default
    )
    console.log(path, handler, middlewares)
    const router = new Hono()
    if (Array.isArray(middlewares) && middlewares.length > 0) {
      router.use(...middlewares)
    }
    handler(router)
    app.route(route.path, router)
  }

  return app
}
// endregion: Apply file routers

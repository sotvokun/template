import {} from 'hono';

type Head = {
  title?: string;
};

declare module 'hono' {
  interface ContextRenderer {
    // biome-ignore lint/style/useShorthandFunctionType: Type
    // biome-ignore lint/suspicious/noExplicitAny: Type
    (params: string | Promise<string>, head?: Head): Response | Promise<Response>;
  }
}

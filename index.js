/**
 * Host half of dsh-skin-anthropic.
 *
 * The skin is pure client-side colour: no service to provide, nothing to
 * register. The bundle patch still inserts this entry so the host fiber exists
 * and the client bundle is mounted; `apply` is intentionally empty.
 */
export const name = "dsh-skin-anthropic";

/** No host behaviour. */
export function apply() {}

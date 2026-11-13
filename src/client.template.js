// dsh-skin-anthropic — client half.
//
// Anthropic's paper palette painted onto the DeepSeek Harness design tokens.
// The whole skin is one stylesheet: it re-declares the --dsw-static-* colour
// ladder, and every --dsw-alias-* token (surfaces, labels, borders, buttons,
// bubbles, popovers) inherits from those rungs.
//
// It deliberately owns no typography: the stylesheet carries colour values only
// and never a typeface, size or weight, so an installed Anthropic
// Sans/Serif/Mono setup keeps working exactly as ui-theme configured it.
//
// Scope: body[data-dsh-skin="anthropic"], set on mount and removed on dispose,
// so unloading the bundle restores the stock look with no residue.
window.__ModuleLoader__.load({
    id: "dsh-skin-anthropic",
    factory: (require) => {
        const module = { exports: {} };
        const exports = module.exports;

        /** Body attribute that scopes every rule in the stylesheet. */
        const SKIN_ATTRIBUTE = "data-dsh-skin";
        /** Value selecting this skin. */
        const SKIN_VALUE = "anthropic";

        /** Generated palette — see scripts/build-tokens.py. */
        const CSS = /* __TOKENS_CSS__ */ "";

        /**
         * Mount the stylesheet and scope the document to it. Both are owned by
         * the plugin fiber, so the skin comes back after a hot reload and
         * disappears cleanly when the bundle is unloaded.
         * @param ctx - client cordis context.
         */
        function apply(ctx) {
            ctx.effect(() => {
                const tag = document.createElement("style");
                tag.dataset.dshSkin = SKIN_VALUE;
                tag.textContent = CSS;
                document.head.append(tag);
                if (document.body) document.body.setAttribute(SKIN_ATTRIBUTE, SKIN_VALUE);
                return () => {
                    tag.remove();
                    if (document.body) document.body.removeAttribute(SKIN_ATTRIBUTE);
                };
            }, "dsh-skin-anthropic: palette");
        }

        exports.apply = apply;
        /** No client services are required: the skin only touches the document. */
        exports.inject = [];
        return module.exports;
    },
});

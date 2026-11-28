// The one SVGO config for making and reviewing icons (svg-icons optimizes with
// it, devicon-icon-review checks against it). It follows devicon's SVGOMG
// guide (wiki "Optimizing icons": multipass, every feature except "Remove
// xmlns", "Round/rewrite number lists" and "Replace duplicate elements with
// links"), with these choices:
// - precision 3, SVGOMG's default: lower precision gives icomoon glyph
//   artifacts (devicons/devicon#2380)
// - colours stay #hex (devicon validation rejects names like "red")
// - <style> classes are inlined even when used more than once, so dropping
//   the <style> element can't lose colours
// - raster <image>s are kept: validation should fail on them instead of the
//   icon silently coming out blank
// - xlink:href stays (older renderers)
// SVGO can still break a font glyph, so check font versions with a font
// preview (devicon's peek-bot) after optimizing.
module.exports = {
  multipass: true,
  floatPrecision: 3,
  plugins: [
    { name: 'preset-default', params: { overrides: {
      removeViewBox: false,
      inlineStyles: { onlyMatchedOnce: false },
      convertColors: { shortname: false },
      // short ids; the scripts then prefix them with the file name
      cleanupIds: { minify: true },
    } } },
    'removeDimensions',
    'removeStyleElement',
    'convertStyleToAttrs',
    'removeScriptElement',
    'removeOffCanvasPaths',
    'convertOneStopGradients',
    { name: 'removeAttrs', params: { attrs: 'svg:(x|y)' } },
  ],
};

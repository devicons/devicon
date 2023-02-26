module.exports = {
  plugins: [
    {
      name: 'preset-default'
    },
    {
      name: 'removeDimensions',
      params: {
        overrides: {
          removeDimensions: true,
        }
      }
    },
    {
      name: 'removeScriptElement',
      params: {
        overrides: {
          removeScriptElement: true,
        }
      }
    },
    {
      name: "removeAttrs",
      params: {
        attrs: [
          'path:fill:none'
        ]
      }
    }
  ]
};

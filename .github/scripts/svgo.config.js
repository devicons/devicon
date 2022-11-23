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
      name: 'convertStyleToAttrs',
      params: {
        overrides: {
          convertStyleToAttrs: true,
        }
      }
    },
    {
      name: 'removeRasterImages',
      params: {
        overrides: {
          removeRasterImages: true,
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
          'path:fill:none',
          'xml.space',
          'enable-background',
          '^data.+',
          'stroke.*',
          'fill-rule',
          'clip-rule'
        ]
      }
    }
  ],
};

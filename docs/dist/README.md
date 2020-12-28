# About `/dist`

This folder contains copied versions of `fonts`, `stylesheets` and `svg` by the root directory of this repository.
It's copied by execution of the custom gulp command:
```gulp
gulp publishDocs
```

This action is run via a GitHub workflow step in `build_icons.yml`

Those copied results in this `dist` folder are required for showing a public available GitHub page which 
is served via the `/docs` directory (where our source is stored outside the `/docs` directory).

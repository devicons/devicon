<h1>Contributing to Devicon</h1>
<p>
First of all, thanks for taking the time to contribute! This project can only grow and live by your countless contributions. To keep this project maintainable, we have developed some guidelines for our contributors.
</p>

<h2>Table of Content</h2>
<ul>
  <li><a href="#terms">Terms</a></li>
  <li><a href="#overview">Overview on Submitting Icon</a></li>
  <li><a href="#versionNaming">Naming Conventions</a></li>
  <li><a href="#svgStandards">SVG Standards</a></li>
  <li><a href="#orgGuidelines">Organizational Guidelines</a></li>
  <li><a href="#updateDevicon">Updating the <code>devicon.json</code></a></li>
  <li><a href="#example">Example</a></li>
  <li><a href="#requestingIcon">Requesting An Icon</a></li>
  <li><a href="#teams">Maintainer/Reviewer/Teams</a></li>
  <li><a href="#buildScript">Regarding the Build Script</a></li>
  <li><a href="#discordServer">Discord server</a></li>
  <li><a href="#release">Release strategy, conventions, preparation and execution</a></li>
</ul>

<hr>
<h2 id="terms">Terms</h2>
<p>Here are some terms that we will use in this repo: </p>
<ol>
  <li>"Technology" is used to describe a software, libraries, tool, etc...</li>
  <li>"Icon" refers to the svgs and icons version of a technology as a whole.</li>
  <li>"SVG/<code>svg</code>" refers to the <code>svg</code> versions of the Icons.</li>
  <li>"icon" (lowercase) refers specficially to the font icon versions of the Icons.</li>
</ol>

<hr>
<h2 id="overview">Overview on Submitting Icons</h2>
<p>Here is what you have to do to submit your icons to the repo.</p>
<ol>
  <li>Create the svgs for each <a href="#versionNaming"> svg versions </a> that you have</li>
  <li>Put the svgs of each Icon into its own folders in <code>/icons</code> </li>
  <li><a href="#updateDevicon">Update the <code>devicon.json</code> to include the new Icon</a> </li>
  <li>Create a separated pull request (PR) towards the <code>develop</code> branch for each Icon.</li>
  <li>Include the name of the Icon in the pull request title in this format: <code>new icon: <i>Icon name</i> (<i>versions</i>)</code> </li>
  <li><i>Optional</i>: Add images of the new svg(s) to the description of the pull request. This would help speed up the review process </li>
  <li><i>Optional</i>: Reference the issues regarding the new icon. </li>
  <li>Wait for a maintainer to review your changes. They will run a script to check your icons.</li>
  <li>If there are no issues, they will accept your pull request and merge it using <a href="https://github.com/devicons/devicon/discussions/470">squash merging</a>. If there are any problems, they will let you know and give you a chance to fix it.</li>
</ol>

<hr>
<h2 id='versionNaming'>Versions and Naming Conventions</h2>
<p>For the technology name, make the file and folder name lowercase and concatenate them. For example:</p>
<ul>
  <li>AngularJS becomes <code>angularjs</code> or just <code>angular</code></li>
  <li>Amazon Web Services becomes <code>amazonwebservices</code></li>
  <li>Microsoft SQL Server becomes <code>microsoftsqlserver</code></li>
</ul>

<p>Each icon/svg can come in different versions. So far, we have:</p>
<ul>
  <li><b>original</b>: the original logo. Can contain multiple colors. <a href="https://github.com/devicons/devicon/blob/master/icons/amazonwebservices/amazonwebservices-original.svg"> Example </a> </li>
  <li><b>original-wordmark</b>: similar to the above but must contain the name of the technology.<a href="https://github.com/devicons/devicon/blob/master/icons/amazonwebservices/amazonwebservices-original-wordmark.svg"> Example </a></li>
  <li><b>plain</b>: a one-color version of the original logo.<a href="https://github.com/devicons/devicon/blob/master/icons/android/android-plain.svg"> Example </a></li>
  <li><b>plain-wordmark</b>: a one-color version of the original logo but with wordmark.<a href="https://github.com/devicons/devicon/blob/master/icons/android/android-plain-wordmark.svg"> Example </a></li>
  <li><b>line</b>: a one-color, line version of the original logo.<a href="https://github.com/devicons/devicon/blob/master/icons/apache/apache-line.svg"> Example </a></li>
  <li><b>line-wordmark</b>: a one-color, line version of the original logo but with wordmark.<a href="https://github.com/devicons/devicon/blob/master/icons/apache/apache-line-wordmark.svg"> Example </a></li>
</ul>
<p> Notes <p>
<ul>  
  <li>
    You don't need to have 6 versions for each icon. An icon can only have one or two versions available. Just keep in mind that the minimum is 1 and the maximum 6 (for now). You must also have at least one version that can be make into an icon.
  </li>
  <li>
    The <b>plain</b> and <b>line</b> versions (with or without wordmark) are designed to be available in the final icon font.
  </li>
  <li>
    The <b>original</b> version are only available in svg format, so they do not need to be as simple and can contain numerous colors.
  </li>
  <li>
    Some icons are really simple (ex. Apple), so the original version can be used as the plain version and as the icon font. In this case, you'll only need to make one of the version (either "original" or "plain"). You can then add an alias in the <code>devicon.json</code> so they can be found with either the "original" or "plain" naming convention. Note: this only applies to font icon versions only, not the SVG versions.
  </li>
</ul>

<hr>
<h2 id='svgStandards'>SVG Standards</h2>
<p>Before you submit your logos/svgs, please ensure that they meet the following standard:</p>
<ul>
  <li>The background must be transparent.</li>
  <li>The svg name follows this convention: <code>(Technology name)-(original|plain|line)(-wordmark?).</code></li>
  <li>The <b>plain</b> and <b>line</b> versions (with or without wordmark) need to stay as simple as possible. They must have only one color and the paths are united. We will strip the color when turning it into icons so they can have any color.
  </li>
  <li>Optimize/compress your SVGs. You can use a service like <a href="https://compressor.io/">compressor</a> or <a href="https://petercollingridge.appspot.com/svg-editor">SVG Editor</a>.</li>
  <li>The icon's strokes and texts must be fills. This is to satisfy our conversion website's <a href="https://icomoon.io/#docs/stroke-to-fill">requirements.</a></li>
  <li>Each <code>.svg</code> file contains one version of an icon in a <code>0 0 128 128</code> viewbox. You can use a service like <a href="https://www.iloveimg.com/resize-image/resize-svg">resize-image</a> for scaling the svg.</li>
  <li>The <code>svg</code> element does not need the <code>height</code> and <code>width</code> attributes. However, if you do use it, ensure their values are either <code>"128"</code> or <code>"128px"</code>. Ex: <code>height="128"</code></li>
  <li>Each <code>.svg</code> must use the <code>fill</code> attribute instead of using <code>classes</code> for colors. See <a href="https://github.com/devicons/devicon/issues/407">here</a> for more details.</li>
  <li>The naming convention for the svg file is the following: <code>(Technology name)-(original|plain|line)(-wordmark?).</code></li>
</ul>

<hr>
<h2 id='orgGuidelines'>Organizational Guidelines</h2>
<ul>
  <li>Each icon has its own folder located in the <code>icons</code> folder</li>
  <li>Each folder <i>may</i> contain one <code>.eps</code> file</li> (optional)
  <li>The <code>.eps</code> file should contains all available versions of an icon. Each version is contained in a 128px by 128px artboard</li>
  <li>Each folder must contain all the <code>.svg</code> files for the Icon</li>
</ul>

<hr>
<h2 id='updateDevicon'> Updating the <code>devicon.json</code> </h2>
<p>
  Before you open a PR into Devicon, you must update the <code>devicon.json</code>. This is essential for our build script to work and to document your work.
</p>
<p>
  Here is the object that each of your Icon must have:
</p>

<pre>
  <code>
    {
        "name": string, // the official name of the technology. Must be lower case, no space and don't have the dash '-' character.
        "tags": string[], // list of tags relating to the technology for search purpose
        "versions": {
            "svg": VersionString[], // list the svgs that you have 
            "font": VersionString[] // list the fonts acceptable versions that you have
        },
        "color": string, // the main color of the logo. Only track 1 color
        "aliases": AliasObj[] // keeps track of the aliases for the font versions ONLY
    }
  </code>
</pre>

<p>
  Here is what VersionString means:
</p>
<ol>
  <li> It's the version part of an <code>svg</code> file's name</li>
  <li> If you have "html5-original", the version string would be "original" </li>
  <li> If you have "react-line-wordmark", the version string would be "line-wordmark" </li>
  <li> See <a href="#versionNaming">naming conventions section</a> for more details </li>
</ol>

<p>
  Here is the AliasObj interface:
</p>
<pre>
  <code>   
    {
        "base": VersionString, // the base version
        "alias": VersionString // the alias version that's similar to the base version
    }
  </code>
</pre>
<hr>

<h2 id='example'>Example </h2>
<p>
As an example, let's assume you have created the svgs for Redhat and Amazon Web Services logos.
</p>
<p>For the Redhat svg, you have the "original", "original-wordmark", "plain", and "plain-wordmark" versions. </p>
<p>For the Amazon Web Services svgs, you have the "original", "original-wordmark", "plain-wordmark" versions. The "original" version is simple enough to be a "plain" version as well. Note that we are not using the acronym AWS.</p>
<ol>
  <li>
    Put the svgs for each logo that you have into its own folders in <code>/icons</code>
    <ul>
      <li>This means you would create two folders: one for <code>amazonwebservices</code> and one for <code>redhat</code></li>
      <li><b>Note</b>: don't do this in the same commits; we want to have each Icon in its own PR.</li>
    </ul>
  </li>
  <li>
    <a href="#updateDevicon">Update the <code>devicon.json</code></a>
    <ul>
      <li>For <code>redhat</code>, you would do this 
        <pre>
          <code>
            {
              "name": "redhat",
              "tags": [
                "server",
                "linux"
              ],
              "versions": {
                "svg": [ // here are the versions that are available in svgs
                  "original",
                  "original-wordmark",
                  "plain",
                  "plain-wordmark"
                ],
                "font": [ // here are the versions that will be used to create icons
                  "plain",
                  "plain-wordmark"
                ]
              },
              "color": "#e93442", // note the '#' character
              "aliases": [] // no aliases in this case
            },
          </code>
        </pre>
      </li>
      <li>For the <code>amazonwebservices</code>, you would do this 
        <pre>
          <code>
            {
              "name": "amazonwebservices", 
              "tags": [
                "cloud",
                "hosting",
                "server"
              ],
              "versions": {
                "svg": [ // here are the versions that are available in svgs
                  "original",
                  "original-wordmark",
                  "plain-wordmark"
                ],
                "font": [ // here are the versions that will be used to create icons
                  "original", // "original" is simple enough to be used as the plain icon so we'll add "plain" to the aliases below
                  "plain-wordmark",
                  // note that the alias "plain" is not listed here. It must be listed in the `aliases` attribute
                ]
              },
              "color": "#F7A80D", // note the '#' character
              "aliases": [
                {
                    "base": "original", // here is the base version that we will upload to Icomoon
                    "alias": "plain" // this is its alias. Our script will create a reference so users can search using "original" or "plain" for this icon
                    // note that you don't provide aliases for the svg version. If "original" can't be made into a font, there's no need to provide it with a plain alias
                }
              ]
            }
          </code>
        </pre>
      </li>
    </ul>
  </li>
  <li>Create a separate pull request (PR) for each Icon.
    <ul>
      <li>This means you would have to create two PRs</li>
      <li>For Amazon Web Services, the branch name would be icons/amazonwebservices. </li>
      <li>For Redhat, the branch name would be icons/redhat. </li>
    </ul>
  </li>
  <li>
    Include the name of the icon in the pull request. Follow this format: "new icon: <i>Icon name</i> (<i>versions</i>}})"
    <ul>
      <li>For Amazon Web Services, your PR title should be "new icon: amazonwebservices (original, original-wordmark, plain-wordmark)"</li>
      <li>For Redhat, your PR title should be "new icon: redhat (original, original-wordmark, plain, plain-wordmark)"</li>
    </ul>
  </li>
  <li>For the rest of the steps, you can follow <a href="#overview">Overview on Submitting Icon</a></li>
</ol>

<hr>
<h2 id='requestingIcon'>Requesting an Icon</h2>
<p>To request an icon, you can create an issue in the repo. Please follow these simple guidelines:</p>
<ul>
  <li>Search for other issues already requesting the icon</li>
  <li>If an issue doesn't exist, create an issue naming it "Icon request: <i>name-of-the-icon</i>". </li>
  <li>Please create a separate issues for each icon</li>
  <li>Optional: include links where the icon can be found</li>
</ul>

<hr>
<h2 id='teams'>Maintainer/Reviewer/Teams</h2>
<p>
    Devicon is living by it's contributors and <a href="https://github.com/orgs/devicons/people">maintainers</a>. Everyone can and is asked to contribute to this project. 
    You <b>don't</b> have to be in a team to contribute!
</p>
<p>
    The branches <code>master</code> and <code>develop</code> are protected branches and only members
    with corresponding permissions (see teams below) are able to push changes to them.
    Additional branches <b>must</b> follow the pattern <code><i>username</i>/feature/<i>description</i></code>.
    The <code>/feature/</code> indicates that a change is made to existing code (regardless
    if it's a fix, refactor or actual feature). The naming convention is based on the <i>gitflow</i>-workflow.
</p>
<p>For organisational purposes we introduced <a href="https://github.com/orgs/devicons/teams">teams</a> with permissions and responsibilities:</p>
<dl>
    <dt>Supporter (@devicons/supporter)</dt>
    <dd>
        Members of this team are responsible for reviewing pull request (auto assigned), managing issues and preparing the upcoming release.<br />
        Supporters have <code>Write</code> access to the repository (allowing them to create own branches) 
        and are allowed to push changes to the <code>develop</code> branch (pull request and status checks required).
    </dd>
    <dt>Maintainer (@devicons/maintainer)</dt>
    <dd>
        Maintainer role inherits from the 'Supporter' role and adds <code>Maintainer</code> permission
        to the repository.
        Members of this team are allowed to publish a new release (push <code>master</code> branch after pull
        request and status checks).
    </dd>
</dl>
<p>
    Wanna join the team? Please <a href="https://github.com/devicons/devicon/discussions/new">open a public discussion</a> where
    you introduce yourself.<br />
    New member requests have to be approved by all active members of the team <b>Maintainer</b>. Every member 
    of this team has a veto permission to reject a new member.<br />
</p>

<hr>
<h2 id='buildScript'>Regarding The Build Script</h2>
<p>To make adding icons easier for repo maintainers, we rely on GitHub Actions, Python, Selenium, and Gulp to automate our tasks.</p>
<p>So far, the tasks in the build script are:</p>
<ul>
  <li>Upload svgs to <a href="https://icomoon.io/app/#/select">icomoon.io</a> and get the icons back. For details, see <a href="https://github.com/devicons/devicon/issues/252"> the original disscussion</a>, <a href="https://github.com/devicons/devicon/pull/268">this PR that introduce the feature</a> and <a href="https://github.com/devicons/devicon/issues/300">the final changes to it.</a></li>
  <li>Build, combine, and minify CSS files. For details, see <a href="https://github.com/devicons/devicon/pull/290">this</a></li>
</ul>
<p>There are also other tasks that we are automating, such as:</p>
<ul>
  <li>Ensure code quality is up to standard</li>
  <li>Upload svgs to <a href="https://icomoon.io/app/#/select">icomoon.io</a> and take a screenshot to check that it looks good.
  <li>Comment on the PR so maintainers don't have to manually upload icon result.</li>
  <li>Publishing a new release to <a href="https://www.npmjs.com/package/devicon">npm</a>; See <a href="https://github.com/devicons/devicon/issues/288">#288</a></li>
</ul>

<h2 id="discordServer">Discord server</h2>
<p>
We are running a Discord server. You can go here to talk, discuss, and more with the maintainers and other people, too. Here's the invitation: https://discord.gg/hScy8KWACQ. If you don't have a GitHub account but want to suggest ideas or new icons, you can do that here in our Discord channel.
<b>Note that the Discord server is unofficial, and Devicons is still being maintained via GitHub.</b>
</p>

<h2 id='release'>Release strategy, conventions, preparation and execution</h2>
<h5>Release strategy</h5>
<p>Devicon does not follow a strict release plan. A new release is depended on current amount of contributions, required bugfixes/patches and will be discussed by the team of maintainers.</p>
<p>Generally speaking: A new release will be published when new icons are added or a bug was fixed. When it's predictable that multiple icons are added in a foreseeable amount of time they are usually wrapped together.</p>
<h5>Conventions</h5>
<p>The version naming follows the rules of <a href="https://semver.org/">Semantic Versioning</a>. Given a version number MAJOR.MINOR.PATCH, increment the:</p>
<ul>
    <li>MAJOR version when you make incompatible API changes,</li>
    <li>MINOR version when you add functionality <b>(like a new icon)</b> in a backwards compatible manner, and</li>
    <li>PATCH version when you make backwards compatible bug fixes.</li>
</ul>

<h5>Release preparation and execution</h5>
<ol>
    <li>Define the next release version number based on the conventions</li>
    <li>Checkout <code>development</code> as <code>draft-release</code> branch</li>
    <li>Bump the package version using <code>npm version v<i>MAJOR</i>.<i>MINOR</i>.<i>PATCH</i> -m "bump npm version to v<i>MAJOR</i>.<i>MINOR</i>.<i>PATCH</i>"</code>  (see <code><a href="https://github.com/devicons/devicon/pull/497">#487</a></code>)</li>
    <li>Push the branch <code>draft-release</code></li>
    <li>Manually trigger the workflow <code><a href="https://github.com/devicons/devicon/actions/workflows/build_icons.yml">build_icons.yml</a></code> (which has a <code>workflow_dispatch</code> event trigger) and select the branch <code>draft-release</code> as target branch. This will build a font version of all icons using icomoon and automatically creates a pull request to merge the build result back into <code>draft-release</code></li>
    <li>Review and approve the auto-create pull request created by the action of the step above</li>
    <li>Create a pull request towards <code>development</code>. Mention the release number in the pull request title and add information about all new icons, fixes, features and enhancements in the description of the pull request. Take the commits as a guideline. It's also a good idea to mention and thank all contributions who participated in the release (take description of <code><a href="https://github.com/devicons/devicon/pull/504">#504</a></code> as an example).</li>
    <li>Wait for review and approval of the pull request (<b>DON'T</b> perform a squash-merge)</li>
    <li>Once merged create a pull request with BASE <code>master</code> and HEAD <code>development</code>. Copy the description of the earlier pull request.</li>
    <li>Since it was already approved in the 'development' stage a maintainer is allowed to merge it (<b>DON'T</b> perform a squash-merge).</li>
    <li>Create a <a href="https://github.com/devicons/devicon/releases/new">new release</a> using v<i>MAJOR</i>.<i>MINOR</i>.<i>PATCH</i> as tag and release title. Use the earlier created description as description of the release.</li>
    <li>Publishing the release will trigger the <a href="/.github/workflows/npm_publish.yml">npm_publish.yml</a> workflow which will execute a <code>npm publish</code> leading to a updated <a href="https://www.npmjs.com/package/devicon">npm package</a> (v<i>MAJOR</i>.<i>MINOR</i>.<i>PATCH</i>).</li>
</ol>
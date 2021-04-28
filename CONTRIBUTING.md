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
  <li><a href="#buildScript">The Build Script: how it works and its quirks</a></li>
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
  <li>A bot will check your SVGs. If there are any errors, please fix them as instructed.</li>
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
        // the official name of the technology. Must be lower case, no space and don't have the dash '-' character.
        "name": string, 

        // list of tags relating to the technology for search purpose
        "tags": string[], 

        // keep tracks of the different versions that you have.
        "versions": {
            // list the svgs that you have 
            "svg": VersionString[], 

            // list the fonts acceptable versions that you have
            "font": VersionString[] 
        },

        // the main color of the logo. Only track 1 color
        "color": string, 

        // keeps track of the aliases for the font versions ONLY
        // see the <a href="#example">Example</a> section for more details
        // NOTE: this attribute is not required from now on (see <a href='https://github.com/devicons/devicon/discussions/465'>this</a>)
        // it is only being kept for backward compatibility
        "aliases": AliasObj[] 
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
<h2 id='buildScript'>The Build Script: how it works and its quirks</h2>
<p>We rely on GitHub Actions, Python, Selenium, Imgur, and Gulp to automate our tasks. Please feel free to take a look at the workflow files. The codes should be clear enough to follow along.</p>
<p>So far, the tasks in the build script are:</p>
<ul>
  <li>Upload svgs to <a href="https://icomoon.io/app/#/select">icomoon.io</a> and get the icons back. For details, see <a href="https://github.com/devicons/devicon/issues/252"> the original disscussion</a>, <a href="https://github.com/devicons/devicon/pull/268">this PR that introduce the feature</a> and <a href="https://github.com/devicons/devicon/issues/300">the final changes to it.</a> Used by <b>peek-bot</b> and <b>build-bot</b>.</li>
  <li>Preview what an svg would look like as an icon using the upload svgs script (see <a href="https://github.com/devicons/devicon/pull/412">this</a>). Used by <b>peek-bot</b>.</li>
  <li>Build, combine, and minify CSS files. For details, see <a href="https://github.com/devicons/devicon/pull/290">this</a>. Used by <b>build-bot</b>.</li>
  <li>Send screenshots to Imgur and upload it to a PR. See <a href="https://github.com/devicons/devicon/pull/398">the PR for the Imgur action</a> and <a href="https://github.com/devicons/devicon/pull/481"> the PR for uploading the pictures to a PR. Used by <b>peek-bot</b> and <b>build-bot</b>.</a>
  <li>Ensure code quality is up to standard</li>
  <li>Comment on the PR so maintainers don't have to manually upload icon result. Used by <b>peek-bot</b> and <b>build-bot</b>.</li>
  <li>Publishing a new release to <a href="https://www.npmjs.com/package/devicon">npm</a>; See <a href="https://github.com/devicons/devicon/issues/288">#288</a></li>
  <li>Creating a list of features that was added since last release. See <a href="https://github.com/devicons/devicon/discussions/574">this discussion</a> for inception and limitations. </li>
</ul>

<p>There are some bugs that the build scripts might run into. Listed below are the common ones and their solutions</p>
<ol>
  <li><b>No connection could be made because the target machine actively refused it. (os error 10061)</b>
    <ul>
      <li>See <a href="https://github.com/devicons/devicon/runs/2292634069?check_suite_focus=true">this action</a> for an example.</li>
      <li>Caused by Selenium being unable to connect to the Icomoon website. It is unknown why this happens but the hypothesis is Icomoon blocks Selenium's multiple connection request and treats them as bots. See <a href="https://github.com/devicons/devicon/pull/544#issuecomment-812147713">this</a>.</li>
      <li>Solution: wait for a few minutes and rerun the script. Repeat until it works.</li>
    </ul>
  </li>
  <li><b>SHA Integrity</b>
    <ul>
      <li>See <a href="https://github.com/devicons/devicon/runs/2310036084?check_suite_focus=true">this action</a> for an example.</li>
      <li>Caused by the <code>package-lock.json</code>. Most likely the result of a dependabot update but not 100% sure.</li>
      <li>Solution: Remove the <code>package-lock.json</code> and run `npm install` to generate a new file. Commit and push.</li>
    </ul>
  </li>
  <li><b>Wrong PR Title</b>
    <ul>
      <li>The <code>bot-peek</code> script relies on the PR title to find the icon that was added in the PR. If the format doesn't match what is specified in <a href="#overview">Overview on Submitting Icon</a>, the bot will fail.</li>
      <li>Solution: Ensure the name of the PR follows the convention.</li>
    </ul>
  </li>
  <li><b>Peek bot fails when an icon is updated</b>
    <ul>
      <li>See <a href="https://github.com/devicons/devicon/pull/554">this PR</a> for an example.</li>
      <li>The <code>bot-peek</code> script compares the <code>devicon.json</code> and <code>icomoon.json</code> to limit the icon uploading process. An update in the repo won't change anything in the <code>devicon.json</code> and <code>icomoon.json</code> so the script would report that nothing is found.</li>
      <li>Solution: Follow the steps laid out <a href="https://github.com/devicons/devicon/pull/554#issuecomment-816860577">here</a></li>
    </ul>
  </li>
  <li><b>Icon created by Icomoon contains strange lines that aren't in the SVG</b>
    <ul>
      <li>See <a href="https://github.com/devicons/devicon/pull/532">this PR</a>'s peek result.</li>
      <li>This is caused by a bug in Icomoon's parser (see <a href="https://github.com/devicons/devicon/pull/532#issuecomment-827180766">this</a>).</li>
      <li>Solution: Luckily this is an extremely rare case. Try remake the svg in a different way (using different paths/shapes) and test using Icomoon.</li>
    </ul>
  </li>
</ol>

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
    <li>Create a pull request towards <code>development</code>. Mention the release number in the pull request title (like "Build preparation for release v<i>MAJOR</i>.<i>MINOR</i>.<i>PATCH</i>).
      <ul> 
        <li>
        Add information about all new icons, fixes, features and enhancements in the description of the pull request. 
        </li>
        <li>
        Take the PRs/commits as a guideline. It's also a good idea to mention and thank all contributions who participated in the release (take description of <code><a href="https://github.com/devicons/devicon/pull/504">#504</a></code> as an example).
        </li>
        <li>
        Rather than doing it manually, you can instead run <code>python ./.github/scripts/get_release_message.py $GITHUB_TOKEN</code> locally. Pass in your GitHub Personal Access Token for <code>$GITHUB_TOKEN</code> and you should see the messages. You can also use the `workflow_dispatch` trigger in the GitHub Actions tab.
        </li>
      </ul>
    </li>
    <li>Wait for review and approval of the pull request (you can perform a squash-merge)</li>
    <li>Once merged create a pull request with BASE <code>master</code> and HEAD <code>development</code>. Copy the description of the earlier pull request.</li>
    <li>Since it was already approved in the 'development' stage a maintainer is allowed to merge it (<b>DON'T</b> perform a squash-merge).</li>
    <li>Create a <a href="https://github.com/devicons/devicon/releases/new">new release</a> using v<i>MAJOR</i>.<i>MINOR</i>.<i>PATCH</i> as tag and release title. Use the earlier created description as description of the release.</li>
    <li>Publishing the release will trigger the <a href="/.github/workflows/npm_publish.yml">npm_publish.yml</a> workflow which will execute a <code>npm publish</code> leading to a updated <a href="https://www.npmjs.com/package/devicon">npm package</a> (v<i>MAJOR</i>.<i>MINOR</i>.<i>PATCH</i>).</li>
</ol>

<script>
import { latestVersion } from "$lib/stores/iconStore"
</script>

<footer
  class="bg-base-300 border-t border-gray-200 bg-white py-8 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-400"
>
  <div class="base-container flex flex-col gap-4">
    <div class="font-damion flex flex-row gap-2 text-4xl text-green-500">
      <i class="devicon-devicon-plain colored"></i>
      Devicon
      <span class=" block sm:mt-auto sm:inline">v{$latestVersion}</span>
    </div>

    <p>
      All product names, logos, and brands are property of their respective owners. All company,
      product and service names used in this website are for identification purposes only. Usage of
      these names, logos, and brands does not imply endorsement of Devicon or its members. All
      icons/SVGs in this project are not monetized in anyway. It is up to the user to use the logo
      properly according to the company/group's brand policy. Usage of this site or any icons/SVGs
      from Devicon means acknowledgement of these conditions.
    </p>
    <p>
      If you have any legal concerns regarding copyrights or want to report an abuse, please reach
      out to us at <a href="mailto:info@devicon.dev" target="_blank" class="underline"
        >info@devicon.dev</a
      > . Any code/logo contributions should be made through our GitHub repository.
    </p>
    <p>
      Originally created by <a href="https://github.com/konpa" target="_blank" class="underline"
        >Konpa</a
      >
      (under
      <a
        href="https://github.com/devicons/devicon/blob/master/LICENSE"
        target="_blank"
        class="underline"
      >
        MIT License
      </a>
      ) and supported by various
      <a
        href="https://github.com/devicons/devicon/graphs/contributors"
        target="_blank"
        class="underline"
      >
        contributors
      </a> .
    </p>
    <p>
      Final font build with <a href="https://icomoon.io/" target="_blank" class="underline"
        >Icomoon</a
      >
    </p>

    <div class="flex flex-col gap-2 pt-2">
      <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200">
        Thanks to all our contributors!
      </h3>
      <p class="text-sm text-gray-600 dark:text-gray-400">
        Devicon would not be possible without you. Thanks for contributing!
      </p>
      <a
        href="https://github.com/devicons/devicon/graphs/contributors"
        target="_blank"
        rel="noopener noreferrer"
      >
        <img
          src="https://contrib.rocks/image?repo=devicons/devicon"
          alt="Devicon Contributors"
          loading="lazy"
          class="max-w-full h-auto"
        />
      </a>
      <p class="text-xs text-gray-500 dark:text-gray-400">
        Made with <a
          href="https://contrib.rocks"
          target="_blank"
          rel="noopener noreferrer"
          class="underline"
          >contrib.rocks</a
        >.
      </p>
    </div>
  </div>
</footer>

<style>
  .font-damion {
    font-family: 'Damion', Times, serif;
  }
</style>

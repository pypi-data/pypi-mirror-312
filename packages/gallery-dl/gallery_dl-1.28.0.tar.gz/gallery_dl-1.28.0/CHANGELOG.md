## 1.28.0 - 2024-11-30
### Changes
- [common] disable using environment network settings by default (`HTTP_PROXY`, `.netrc`, …)
  - disable `trust_env` session attribute
  - disable `Authorization` header injection from `.netrc` auth ([#5780](https://github.com/mikf/gallery-dl/issues/5780), [#6134](https://github.com/mikf/gallery-dl/issues/6134), [#6455](https://github.com/mikf/gallery-dl/issues/6455))
  - add `proxy-env` option
- [ytdl] change `forward-cookies` default value to `true` ([#6401](https://github.com/mikf/gallery-dl/issues/6401), [#6348](https://github.com/mikf/gallery-dl/issues/6348))
### Extractors
#### Additions
- [bilibili] add support for `opus` articles ([#2824](https://github.com/mikf/gallery-dl/issues/2824), [#6443](https://github.com/mikf/gallery-dl/issues/6443))
- [bluesky] add `hashtag` extractor ([#4438](https://github.com/mikf/gallery-dl/issues/4438))
- [danbooru] add `artist` and `artist-search` extractors ([#5348](https://github.com/mikf/gallery-dl/issues/5348))
- [everia] add support ([#1067](https://github.com/mikf/gallery-dl/issues/1067), [#2472](https://github.com/mikf/gallery-dl/issues/2472), [#4091](https://github.com/mikf/gallery-dl/issues/4091), [#6227](https://github.com/mikf/gallery-dl/issues/6227))
- [facebook] add support ([#470](https://github.com/mikf/gallery-dl/issues/470), [#2612](https://github.com/mikf/gallery-dl/issues/2612), [#5626](https://github.com/mikf/gallery-dl/issues/5626), [#6548](https://github.com/mikf/gallery-dl/issues/6548))
- [hentaifoundry] add `tag` extractor ([#6465](https://github.com/mikf/gallery-dl/issues/6465))
- [hitomi] add `index` and `search` extractors ([#2502](https://github.com/mikf/gallery-dl/issues/2502), [#6392](https://github.com/mikf/gallery-dl/issues/6392), [#3720](https://github.com/mikf/gallery-dl/issues/3720))
- [motherless] add support ([#2074](https://github.com/mikf/gallery-dl/issues/2074), [#4413](https://github.com/mikf/gallery-dl/issues/4413), [#6221](https://github.com/mikf/gallery-dl/issues/6221))
- [noop] add `noop` extractor
- [rule34vault] add support ([#5708](https://github.com/mikf/gallery-dl/issues/5708), [#6240](https://github.com/mikf/gallery-dl/issues/6240))
- [rule34xyz] add support ([#1078](https://github.com/mikf/gallery-dl/issues/1078), [#4960](https://github.com/mikf/gallery-dl/issues/4960))
- [saint] add support ([#4405](https://github.com/mikf/gallery-dl/issues/4405), [#6324](https://github.com/mikf/gallery-dl/issues/6324))
- [tumblr] add `search` extractor ([#6394](https://github.com/mikf/gallery-dl/issues/6394))
#### Fixes
- [8chan] avoid performing network requests within `_init()` ([#6387](https://github.com/mikf/gallery-dl/issues/6387))
- [bluesky] fix downloads from non-bsky PDSs ([#6406](https://github.com/mikf/gallery-dl/issues/6406))
- [bunkr] fix album names containing `<>&` characters
- [flickr] use `download` URLs ([#6360](https://github.com/mikf/gallery-dl/issues/6360), [#6464](https://github.com/mikf/gallery-dl/issues/6464))
- [hiperdex] update domain to `hipertoon.com` ([#6420](https://github.com/mikf/gallery-dl/issues/6420))
- [imagechest] fix extractors ([#6475](https://github.com/mikf/gallery-dl/issues/6475), [#6491](https://github.com/mikf/gallery-dl/issues/6491))
- [instagram] fix using numeric cursor values ([#6414](https://github.com/mikf/gallery-dl/issues/6414))
- [kemonoparty] update to new site layout ([#6415](https://github.com/mikf/gallery-dl/issues/6415), [#6503](https://github.com/mikf/gallery-dl/issues/6503), [#6528](https://github.com/mikf/gallery-dl/issues/6528), [#6530](https://github.com/mikf/gallery-dl/issues/6530), [#6536](https://github.com/mikf/gallery-dl/issues/6536), [#6542](https://github.com/mikf/gallery-dl/issues/6542), [#6554](https://github.com/mikf/gallery-dl/issues/6554))
- [koharu] update domain to `niyaniya.moe` ([#6430](https://github.com/mikf/gallery-dl/issues/6430), [#6432](https://github.com/mikf/gallery-dl/issues/6432))
- [mangadex] apply `lang` option only to chapter results ([#6372](https://github.com/mikf/gallery-dl/issues/6372))
- [newgrounds] fix metadata extraction ([#6463](https://github.com/mikf/gallery-dl/issues/6463), [#6533](https://github.com/mikf/gallery-dl/issues/6533))
- [nhentai] support `.webp` files ([#6442](https://github.com/mikf/gallery-dl/issues/6442), [#6479](https://github.com/mikf/gallery-dl/issues/6479))
- [patreon] use legacy mobile UA when no `session_id` is set
- [pinterest] update API headers ([#6513](https://github.com/mikf/gallery-dl/issues/6513))
- [pinterest] detect video/audio by block content ([#6421](https://github.com/mikf/gallery-dl/issues/6421))
- [scrolller] prevent exception for posts without `mediaSources` ([#5051](https://github.com/mikf/gallery-dl/issues/5051))
- [tumblrgallery] fix file downloads ([#6391](https://github.com/mikf/gallery-dl/issues/6391))
- [twitter] make `source` metadata extraction non-fatal ([#6472](https://github.com/mikf/gallery-dl/issues/6472))
- [weibo] fix livephoto `filename` & `extension` ([#6471](https://github.com/mikf/gallery-dl/issues/6471))
#### Improvements
- [bluesky] support `main.bsky.dev` URLs ([#4438](https://github.com/mikf/gallery-dl/issues/4438))
- [bluesky] match common embed fixes ([#6410](https://github.com/mikf/gallery-dl/issues/6410), [#6411](https://github.com/mikf/gallery-dl/issues/6411))
- [boosty] update default video format list ([#2387](https://github.com/mikf/gallery-dl/issues/2387))
- [bunkr] support `bunkr.cr` URLs
- [common] allow passing cookies to OAuth extractors
- [common] allow overriding more default `User-Agent` headers ([#6496](https://github.com/mikf/gallery-dl/issues/6496))
- [philomena] switch default `ponybooru` filter ([#6437](https://github.com/mikf/gallery-dl/issues/6437))
- [pinterest] support `story_pin_music` blocks ([#6421](https://github.com/mikf/gallery-dl/issues/6421))
- [pixiv] get ugoira frame extension from `meta_single_page` values ([#6056](https://github.com/mikf/gallery-dl/issues/6056))
- [reddit] support user profile share links ([#6389](https://github.com/mikf/gallery-dl/issues/6389))
- [steamgriddb] disable `adjust-extensions` for `fake-png` files ([#5274](https://github.com/mikf/gallery-dl/issues/5274))
- [twitter] remove cookies migration workaround
#### Metadata
- [bluesky] provide `author[instance]` metadata ([#4438](https://github.com/mikf/gallery-dl/issues/4438))
- [instagram] fix `extension` of apparent `.webp` files ([#6541](https://github.com/mikf/gallery-dl/issues/6541))
- [pillowfort] provide `count` metadata ([#6478](https://github.com/mikf/gallery-dl/issues/6478))
- [pixiv:ranking] add `rank` metadata field ([#6531](https://github.com/mikf/gallery-dl/issues/6531))
- [poipiku] return `count` as proper number ([#6445](https://github.com/mikf/gallery-dl/issues/6445))
- [webtoons] extract `episode_no` for comic results ([#6439](https://github.com/mikf/gallery-dl/issues/6439))
#### Options
- [civitai] add `metadata` option - support fetching `generation` data ([#6383](https://github.com/mikf/gallery-dl/issues/6383))
- [exhentai] implement `tags` option ([#2117](https://github.com/mikf/gallery-dl/issues/2117))
- [koharu] implement `tags` option
- [rule34xyz] add `format` option ([#1078](https://github.com/mikf/gallery-dl/issues/1078))
### Downloaders
- [ytdl] fix `AttributeError` caused by `decodeOption()` removal ([#6552](https://github.com/mikf/gallery-dl/issues/6552))
### Post Processors
- [classify] rewrite - fix skipping existing files ([#5213](https://github.com/mikf/gallery-dl/issues/5213))
- enable inheriting options from global `postprocessor` objects
- allow `postprocessors` values to be a single post processor object
### Cookies
- support Chromium table version 24 ([#6162](https://github.com/mikf/gallery-dl/issues/6162))
- fix GCM pad length calculation ([#6162](https://github.com/mikf/gallery-dl/issues/6162))
- try decryption with empty password as fallback
### Documentation
- update recommended `pip` command for installing `dev` version ([#6493](https://github.com/mikf/gallery-dl/issues/6493))
- update `gallery-dl.conf` ([#6501](https://github.com/mikf/gallery-dl/issues/6501))
### Options
- add `-4/--force-ipv4` and `-6/--force-ipv6` command-line options
- fix passing negative numbers as arguments ([#5262](https://github.com/mikf/gallery-dl/issues/5262))
### Miscellaneous
- [output] use default ANSI colors only when stream is a TTY
- [util] implement `defaultdict` filters-environment
- [util] enable using multiple statements for all `filter` options ([#5262](https://github.com/mikf/gallery-dl/issues/5262))

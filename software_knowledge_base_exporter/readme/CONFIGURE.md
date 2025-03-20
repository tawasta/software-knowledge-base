- Important notes regarding configuration

  - swkb_server, swkb_user and swkb_db system parameters are flagged with noupdate=0 and are designed to be
    overridden with a separate module's data file. be sure that that module has this one in its dependencies. that module
    will be responsible for keeping e.g. host url up to date when/if it changes.
  - swkb_token is flagged with noupdate=1 and is always expected to be configured by hand via UI. If we ever want to change this
    system, move also swkb_token under noupdate=0, and then also the token can be managed in the separate module.

import os
from datetime import datetime, timezone

import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True if 'DEV_FLAG' not in os.environ else False

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        "time_ago",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("time_ago", path=build_dir)


def time_ago(date: datetime, prefix: str = '', key=None):
    """Display time ago from the given time, with live updates using JS (without re-runs)

    Examples:
        just now
        45s
        5m
        15 minutes ago
        3 hours ago
        in 2 months
        in 5 years

    Parameters
    ----------
    date: datetime object
    prefix: optional text to include before the date, e.g. "Created" to show "Created just now"
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    if date is None:
        return
    assert isinstance(date, datetime), f'Expected datetime object, got: {date} ({type(date).__name__})'
    _component_func(
        datetime=date.astimezone(timezone.utc).isoformat(),
        prefix=prefix,
        key=key
    )

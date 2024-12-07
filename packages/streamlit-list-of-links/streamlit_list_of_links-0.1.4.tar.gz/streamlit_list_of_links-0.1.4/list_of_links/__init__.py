import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "list_of_links",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("list_of_links", path=build_dir)


def list_of_links(title, links, key=None):
    """
    A function that interfaces with a private frontend component function.

    This function facilitates interaction with a frontend component by
    passing specified arguments. The arguments include a title and an
    array of links, with an optional key. The function communicates these
    to the frontend and retrieves an initial return value, which is
    configured to be zero by default. This setup allows the returned value
    to be modified if necessary, enabling dynamic user interactions with
    the component.

    Parameters
    ----------
    title : str
        A string to set as the title of the component.
    links : list
        A list containing link elements to be processed by the component.
    key : optional
        An optional parameter for component identification or tracking.

    Returns
    -------
    int
        The initial value returned by the component.
    """
    component_value = _component_func(title=title, links=links, key=key, default=0)
    return component_value

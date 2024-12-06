import pandas
import streamlit as st
from pyzrpc.admin.common import GenZrpc

st.set_page_config(page_title="Nodes", page_icon=":material/table:")
st.title("Nodes")


class Query:
    def __init__(self):
        self._ipaddr: str = ''

    @property
    def ipaddr(self):
        return self._ipaddr

    @ipaddr.setter
    def ipaddr(self, value):
        self._ipaddr = value


class Pagination:

    def __init__(self):
        self._total = 10
        self._page = 1
        self._page_size = 10

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, value):
        self._page = value

    @property
    def total(self):
        return int(self._total / self._page_size) + 1

    @total.setter
    def total(self, value):
        self._total = value

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, value):
        self._page_size = value

    @property
    def skip_no(self):
        return self._page_size * (self._page - 1)


queryObj = Query()
paginationObj = Pagination()

if paginationObj.total == 0:
    paginationObj.total = GenZrpc().db_node_info().get_count({})


def search():
    skip_no = paginationObj.skip_no
    limit = paginationObj.page_size

    query = {}
    if queryObj.ipaddr:
        query['ipaddr'] = queryObj.ipaddr

    count, data = GenZrpc().db_node_info().get_list(
        query=query,
        field={"_id": 0},
        limit=limit,
        skip_no=skip_no
    )

    st.write(data)


def search_code():
    st.sidebar.write("***Search Parameters***")
    input_ipaddr = st.sidebar.text_input(label="ipaddr", placeholder="Please enter ipaddr")
    queryObj.ipaddr = input_ipaddr

    st.sidebar.button("Search", on_click=search())


search_code()

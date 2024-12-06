import streamlit as st

from pyzrpc.admin.common import GenZrpc

st.set_page_config(page_title="Services", page_icon=":material/table:")
st.title("Services")


class Query:
    def __init__(self):
        self._service_ipaddr: str = ''
        self._work_name: str = ''

    @property
    def work_name(self):
        return self._work_name

    @work_name.setter
    def work_name(self, value):
        self._work_name = value

    @property
    def service_ipaddr(self):
        return self._service_ipaddr

    @service_ipaddr.setter
    def service_ipaddr(self, value):
        self._service_ipaddr = value


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
    paginationObj.total = GenZrpc().db_service().get_count({})


def search():
    skip_no = paginationObj.skip_no
    limit = paginationObj.page_size

    query = {}
    if queryObj.service_ipaddr:
        query['service_ipaddr'] = queryObj.service_ipaddr

    if queryObj.work_name:
        query['work_name'] = queryObj.work_name

    count, data = GenZrpc().db_service().get_list(
        query=query,
        field={"_id": 0},
        limit=limit,
        skip_no=skip_no
    )

    st.write(data)


def search_code():
    st.sidebar.write("***Search Parameters***")
    input_ipaddr = st.sidebar.text_input(label="service_ipaddr", placeholder="Please enter service_ipaddr")
    queryObj.service_ipaddr = input_ipaddr

    input_work_name = st.sidebar.text_input(label="work_name", placeholder="Please enter work_name")
    queryObj.work_name = input_work_name

    st.sidebar.button("Search", on_click=search())


search_code()

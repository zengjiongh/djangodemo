"""
自定义的分页组件
1.views中引用组件并使用
from config.utills import pagination
page_obj = pagination.Pagination(request,queryset)
content = {
    "queryset":page_obj.page_queryset,
    "page_string":page_obj.html()
}

2.html中使用分页
<ul class="pagination clearfix">
    {{ page_string }}
</ul>
"""
from django.utils.safestring import mark_safe
from django.http.request import QueryDict
import copy


class Pagination(object):
    def __init__(self, request, queryset, page_parm="page", page_size=10, plus=5):

        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        page = request.GET.get(page_parm, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.page_parm = page_parm
        self.plus = plus
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start:self.end]
        total_count = queryset.count()
        ##总页码数
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count

    def html(self):
        ##计算出。显示当前页的前五页和后五页
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            start_page = self.page - self.plus
            end_page = self.page + self.plus
            if start_page <= 0:
                start_page = 1
                end_page = 2 * self.plus + 1

            if end_page > self.total_page_count:
                start_page = self.total_page_count - 2 * self.plus
                end_page = self.total_page_count
        page_str_list = []
        ##首页
        self.query_dict.setlist(self.page_parm, [1])
        first = '<li><a href="?{}" aria-label="Previous"><span aria-hidden="true">首页</span></a></li>'.format(
            self.query_dict.urlencode())
        page_str_list.append(first)

        ##上一页
        prev_s = self.page - 1
        if prev_s <= 0:
            prev_s = 1
        self.query_dict.setlist(self.page_parm, [prev_s])
        prev = '<li><a href="?{}" aria-label="Previous"><span aria-hidden="true">«</span></a></li>'.format(
            self.query_dict.urlencode())
        page_str_list.append(prev)

        ##页码
        for i in range(start_page, end_page + 1):
            if i == self.page:
                self.query_dict.setlist(self.page_parm, [i])
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                self.query_dict.setlist(self.page_parm, [i])
                ele = '<li class=""><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        ##下一页
        next_s = self.page + 1
        if next_s > self.total_page_count:
            next_s = self.total_page_count
        self.query_dict.setlist(self.page_parm, [next_s])
        next = '<li><a href="?{}" aria-label="NEXT"><span aria-hidden="true">»</span></a></li>'.format(
            self.query_dict.urlencode())
        page_str_list.append(next)

        # 尾页
        self.query_dict.setlist(self.page_parm, [self.total_page_count])
        first = '<li><a href="?{}" aria-label="Previous"><span aria-hidden="true">尾页</span></a></li>'.format(
            self.query_dict.urlencode())
        page_str_list.append(first)

        ##翻页

        search_string = """
           <li>
               <form method="get" style="float: right;width:200px">
                   <div class="input-group">
                       <input type="text" class="form-control" placeholder="搜索页码" name="page" >
                       <span class="input-group-btn">
                       <button class="btn btn-default" type="submit">
                       跳转
                       </button>
                       </span>
                   </div><!-- /input-group -->
               </form>
           </li>
           """
        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))

        return page_string

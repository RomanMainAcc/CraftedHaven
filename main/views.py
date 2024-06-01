from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "CraftedHaven - home page"
        context['content'] = "Furniture store CraftedHaven"
        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "CraftedHaven - about us"
        context['content'] = "About us"
        context['text_on_page'] = (
            "Our furniture is made using the finest materials and meets the highest quality standards.")
        return context

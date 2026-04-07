---
title: Tags
---

# Tags

Browse all drug allergy testing protocols by tag. Click any tag below to see related protocols.

## Tags

{% for tag in config.tags %}
### {{ tag.name }}
{% for page in tag.pages %}
- [{{ page.title }}]({{ page.url }})
{% endfor %}
{% endfor %}

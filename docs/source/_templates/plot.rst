{{ source_code }}

{{ only_html }}
	{# images #}
	{% for img in images %}
	.. figure:: {{ build_dir }}/{{ img.basename }}.{{ default_fmt }}
		{% for option in options -%}
		{{ option }}
		{% endfor %}

		{% if html_show_formats and multi_image -%}
			(
			{%- for fmt in img.formats -%}
			{%- if not loop.first -%}, {% endif -%}
			`{{ fmt }} <{{ dest_dir }}/{{ img.basename }}.{{ fmt }}>`__
			{%- endfor -%}
			)
		{%- endif -%}

		{{ caption }}
	{% endfor %}
	{# source #}
	{% if source_link or (html_show_formats and not multi_image) %}
	(
	{%- if source_link -%}
	`Source code <{{ source_link }}>`__
	{%- endif -%}
	{%- if html_show_formats and not multi_image -%}
		{%- for img in images -%}
		{%- for fmt in img.formats -%}
			{%- if source_link or not loop.first -%}, {% endif -%}
			`{{ fmt }} <{{ dest_dir }}/{{ img.basename }}.{{ fmt }}>`__
		{%- endfor -%}
		{%- endfor -%}
	{%- endif -%}
	)
	{% endif %}

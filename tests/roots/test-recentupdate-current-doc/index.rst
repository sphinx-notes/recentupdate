Recentupdate Current Doc Test
==============================

.. data.render::
   :debug:

   {% for r in load_extra('recentupdate', count=10, current_doc=True) %}
   Commit: {{ r.message[0] }}
   {% endfor %}

Modified content.

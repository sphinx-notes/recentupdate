Recentupdate Basic Test
=======================

.. data.render::
   :debug:

   {% for r in load_extra('recentupdate', count=5) %}
   Commit: {{ r.message[0] }}
   {% endfor %}

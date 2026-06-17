Recentupdate Path Filter Test
=============================

.. data.render::
   :debug:

   {% for r in load_extra('recentupdate', count=10, path='subdir') %}
   Commit: {{ r.message[0] }}
   {% endfor %}

=============
Configuration
=============

The extension provides the following configuration:

.. confval:: recentupdate_count
   :type: int
   :default: 10

   The default count of recent revisions. See :doc:`usage`.

.. confval:: recentupdate_template
   :type: str
   :default: see below

   The default Jinja template of update information. See :doc:`usage`.

   Here is the default value:

   .. code:: jinja

      {% for r in revisions %}
      {{ r.date | strftime }}
        :Author: {{ r.author }}
        :Message: {{ r.message }}

        {% if r.modification %}
        - Modified {{ r.modification | roles("doc") | join(", ") }}
        {% endif %}
        {% if r.addition %}
        - Added {{ r.addition | roles("doc") | join(", ") }}
        {% endif %}
        {% if r.deletion %}
        - Deleted {{ r.deletion | join(", ") }}
        {% endif %}
      {% endfor %}

.. confval:: recentupdate_date_format
   :type: str
   :default: "%Y-%m-%dT"

   The default date format of :ref:`strftime` filter.

.. confval:: recentupdate_exclude_path
   :type: List[str]
   :default: []

   A list of path that should be excluded when looking for file changes. 

.. confval:: recentupdate_exclude_commit
   :type: List[str]
   :default: ["skip-recentupdate"]

   A list of commit message pattern that should be excluded when looking for file changes. 


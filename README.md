# Chef Cookbook Dependency Resolver
A very simple utility I wrote for myself while wrapping my head around some cookbooks.

# Installation
```
# project_path=/tmp/chefdep
# virtualenv ${project_path}
# cd ${project_path}
# git clone https//github.com/baccenfutter/chefdep.git
# ln -s ${project_path}/chefdep/chefdep/chefdep.py /usr/local/bin/chefdep
# ln -s ${project_path}/chefdep/chefdep/chefdep.py /usr/local/bin/chefrevdep
```

# Usage
To get all dependencies of a recipe.
```
# chefdep <path-to-recipe>
```

To get all reverse dependencies of a recipe.
```
# chefrevdep <path-to-recipe>
```


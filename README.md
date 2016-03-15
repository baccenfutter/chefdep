# Chef Cookbook Dependency Resolver
While wrapping my head around the cookbooks of my new employer, I wrote myself this little utility to get a better grasp
of the dependency chains. Feel free to use in case you see fit.

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


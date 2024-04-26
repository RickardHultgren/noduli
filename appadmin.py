# appadmin.py

from gluon.tools import Crud

crud = Crud(db)


@auth.requires_membership('admin')
def user_accounts():
  # Display the number of user accounts
  user_count = db(db.auth_user).count()
  return dict(user_count=user_count)


@auth.requires_membership('admin')
def manage_nodes():
  # Manage nodes, allowing changes and deletions sorted by user

  # Fetch all users
  users = db(db.auth_user).select(orderby=db.auth_user.id)

  # Process form submission for user selection
  form = SQLFORM.factory(Field('selected_user',
                               requires=IS_IN_SET(users, 'id', '%(email)s')),
                         submit_button='Select User')

  if form.process().accepted:
    # Get selected user's nodes
    selected_user_id = form.vars.selected_user
    user_nodes = db(db.node.created_by == selected_user_id).select()

    return dict(form=form, user_nodes=user_nodes)

  return dict(form=form, user_nodes=None)


@auth.requires_membership('admin')
def edit_node():
  # Edit node details

  # Extract node ID from request.args
  node_id = request.args(0)

  # Fetch the node record
  node_record = db.node(node_id)
  if not node_record:
    redirect(URL('default',
                 'index'))  # Redirect to the homepage if node not found

  # Create a form for editing the node
  form = crud.update(db.node, node_id, next='manage_nodes')

  return dict(form=form, node_record=node_record)

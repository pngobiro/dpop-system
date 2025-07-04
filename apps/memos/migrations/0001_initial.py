# Generated by Django 3.2.25 on 2025-07-04 10:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('meetings', '0009_auto_20250702_1316'),
        ('organization', '0003_department_email'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0010_auto_20250702_1222'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('document_management', '0002_auto_20250529_1112'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentThread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('is_internal', models.BooleanField(default=True, help_text='Internal comments visible only to department staff')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Memo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reference_number', models.CharField(db_index=True, max_length=100, unique=True)),
                ('title', models.CharField(max_length=500)),
                ('subject', models.TextField(help_text='Brief subject/summary')),
                ('content', models.TextField(blank=True, help_text='Main memo content')),
                ('is_physical', models.BooleanField(default=False, help_text='Is this a physical memo?')),
                ('is_confidential', models.BooleanField(default=False)),
                ('received_date', models.DateTimeField(blank=True, help_text='Date memo was received (for incoming memos)', null=True)),
                ('dispatch_date', models.DateTimeField(blank=True, help_text='Date memo was dispatched (for outgoing memos)', null=True)),
                ('due_date', models.DateField(blank=True, help_text='Date by which action/response is required', null=True)),
                ('sender_external_name', models.CharField(blank=True, help_text='Name of external sender', max_length=255)),
                ('sender_external_organization', models.CharField(blank=True, help_text='Organization of external sender', max_length=255)),
                ('sender_external_address', models.TextField(blank=True, help_text='Address of external sender')),
                ('recipient_external_name', models.CharField(blank=True, help_text='Name of external recipient', max_length=255)),
                ('recipient_external_organization', models.CharField(blank=True, help_text='Organization of external recipient', max_length=255)),
                ('recipient_external_address', models.TextField(blank=True, help_text='Address of external recipient')),
                ('file_number', models.CharField(blank=True, help_text='Physical file reference number', max_length=100)),
                ('tags', models.CharField(blank=True, help_text='Comma-separated tags for searching', max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('version', models.PositiveIntegerField(default=1)),
                ('is_latest_version', models.BooleanField(default=True)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'permissions': [('can_approve_memos', 'Can approve memos'), ('can_dispatch_memos', 'Can dispatch memos'), ('can_view_confidential_memos', 'Can view confidential memos'), ('can_manage_workflow', 'Can manage memo workflow')],
            },
        ),
        migrations.CreateModel(
            name='MemoCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('color', models.CharField(default='#007bff', help_text='Hex color code', max_length=7)),
                ('icon', models.CharField(default='fas fa-file-alt', help_text='FontAwesome icon class', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Memo Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MemoStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
                ('color', models.CharField(help_text='Hex color code', max_length=7)),
                ('is_final', models.BooleanField(default=False, help_text='Cannot change status after reaching this state')),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0, help_text='Display order')),
            ],
            options={
                'verbose_name_plural': 'Memo Statuses',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='MemoWorkflow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('is_default', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('department', models.ForeignKey(help_text='Department this workflow applies to', on_delete=django.db.models.deletion.CASCADE, to='organization.department')),
            ],
            options={
                'ordering': ['department', 'name'],
                'unique_together': {('department', 'name')},
            },
        ),
        migrations.CreateModel(
            name='PriorityLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('level', models.PositiveIntegerField(help_text='1=Highest, 5=Lowest', unique=True)),
                ('color', models.CharField(help_text='Hex color code', max_length=7)),
                ('description', models.TextField(blank=True)),
                ('response_time_days', models.PositiveIntegerField(blank=True, help_text='Expected response time in days', null=True)),
            ],
            options={
                'ordering': ['level'],
            },
        ),
        migrations.CreateModel(
            name='WorkflowStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('step_order', models.PositiveIntegerField()),
                ('role_required', models.CharField(help_text='Required role/permission for this step', max_length=100)),
                ('is_optional', models.BooleanField(default=False)),
                ('time_limit_days', models.PositiveIntegerField(blank=True, help_text='Time limit for this step in days', null=True)),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='memos.memoworkflow')),
            ],
            options={
                'ordering': ['workflow', 'step_order'],
                'unique_together': {('workflow', 'step_order')},
            },
        ),
        migrations.CreateModel(
            name='ThreadComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_edited', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='memos.commentthread')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='StatusHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(blank=True)),
                ('changed_at', models.DateTimeField(auto_now_add=True)),
                ('changed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('from_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='status_changes_from', to='memos.memostatus')),
                ('memo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_history', to='memos.memo')),
                ('to_status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='status_changes_to', to='memos.memostatus')),
            ],
            options={
                'ordering': ['-changed_at'],
            },
        ),
        migrations.CreateModel(
            name='MemoType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('code', models.CharField(help_text='Short code for reference numbers', max_length=10, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('requires_approval', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('default_workflow', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='default_for_types', to='memos.memoworkflow')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MemoTimeline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(choices=[('created', 'Created'), ('received', 'Received'), ('assigned', 'Assigned'), ('forwarded', 'Forwarded'), ('delegated', 'Delegated'), ('status_changed', 'Status Changed'), ('document_added', 'Document Added'), ('comment_added', 'Comment Added'), ('workflow_step', 'Workflow Step'), ('dispatched', 'Dispatched'), ('completed', 'Completed')], max_length=50)),
                ('description', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('memo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timeline', to='memos.memo')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='MemoDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(choices=[('original', 'Original Document'), ('attachment', 'Attachment'), ('signature', 'Signature/Stamp'), ('response', 'Response Document'), ('version', 'Version')], max_length=50)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document_management.document')),
                ('memo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='memos.memo')),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-uploaded_at'],
            },
        ),
        migrations.AddField(
            model_name='memo',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='memos.memocategory'),
        ),
        migrations.AddField(
            model_name='memo',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='memo',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_memos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='memo',
            name='current_step',
            field=models.ForeignKey(blank=True, help_text='Current step in workflow', null=True, on_delete=django.db.models.deletion.SET_NULL, to='memos.workflowstep'),
        ),
        migrations.AddField(
            model_name='memo',
            name='department',
            field=models.ForeignKey(help_text='Department handling this memo', on_delete=django.db.models.deletion.PROTECT, to='organization.department'),
        ),
        migrations.AddField(
            model_name='memo',
            name='memo_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='memos.memotype'),
        ),
        migrations.AddField(
            model_name='memo',
            name='original_memo',
            field=models.ForeignKey(blank=True, help_text='Reference to original memo if this is a version', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='memos.memo'),
        ),
        migrations.AddField(
            model_name='memo',
            name='priority',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='memos.prioritylevel'),
        ),
        migrations.AddField(
            model_name='memo',
            name='recipient_departments',
            field=models.ManyToManyField(blank=True, related_name='received_memos', to='organization.Department'),
        ),
        migrations.AddField(
            model_name='memo',
            name='recipient_users',
            field=models.ManyToManyField(blank=True, related_name='received_memos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='memo',
            name='sender_internal',
            field=models.ForeignKey(blank=True, help_text='Internal user who sent the memo', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_memos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='memo',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='memos.memostatus'),
        ),
        migrations.AddField(
            model_name='memo',
            name='workflow',
            field=models.ForeignKey(blank=True, help_text='Workflow being followed', null=True, on_delete=django.db.models.deletion.SET_NULL, to='memos.memoworkflow'),
        ),
        migrations.CreateModel(
            name='Delegation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(blank=True)),
                ('instructions', models.TextField(blank=True)),
                ('delegated_at', models.DateTimeField(auto_now_add=True)),
                ('accepted_at', models.DateTimeField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('completed', 'Completed')], default='pending', max_length=20)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delegated_from', to=settings.AUTH_USER_MODEL)),
                ('memo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delegations', to='memos.memo')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delegated_to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-delegated_at'],
            },
        ),
        migrations.AddField(
            model_name='commentthread',
            name='memo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_threads', to='memos.memo'),
        ),
        migrations.CreateModel(
            name='ActionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=100)),
                ('details', models.TextField(blank=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.TextField(blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('memo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action_logs', to='memos.memo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ActionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delegated_memo_actions', to=settings.AUTH_USER_MODEL)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_memo_actions', to=settings.AUTH_USER_MODEL)),
                ('memo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action_items', to='memos.memo')),
                ('priority', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='memos.prioritylevel')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='RelatedMemo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationship_type', models.CharField(choices=[('response_to', 'Response To'), ('follow_up', 'Follow Up'), ('reference', 'References'), ('supersedes', 'Supersedes'), ('related', 'Related')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('from_memo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_memos_from', to='memos.memo')),
                ('to_memo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_memos_to', to='memos.memo')),
            ],
            options={
                'unique_together': {('from_memo', 'to_memo')},
            },
        ),
        migrations.CreateModel(
            name='MemoTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationship_type', models.CharField(choices=[('derived_from', 'Task Derived From Memo'), ('referenced_in', 'Task Referenced in Memo'), ('response_to', 'Task is Response to Memo')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('memo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_tasks', to='memos.memo')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_memos', to='tasks.task')),
            ],
            options={
                'unique_together': {('memo', 'task')},
            },
        ),
        migrations.CreateModel(
            name='MemoMeeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationship_type', models.CharField(choices=[('agenda_item', 'Memo as Agenda Item'), ('follow_up', 'Meeting Follow-up to Memo'), ('referenced_in', 'Memo Referenced in Meeting')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_memos', to='meetings.meeting')),
                ('memo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_meetings', to='memos.memo')),
            ],
            options={
                'unique_together': {('memo', 'meeting')},
            },
        ),
        migrations.AddIndex(
            model_name='memo',
            index=models.Index(fields=['reference_number'], name='memos_memo_referen_b3a161_idx'),
        ),
        migrations.AddIndex(
            model_name='memo',
            index=models.Index(fields=['status', 'department'], name='memos_memo_status__e440a4_idx'),
        ),
        migrations.AddIndex(
            model_name='memo',
            index=models.Index(fields=['received_date'], name='memos_memo_receive_088a92_idx'),
        ),
        migrations.AddIndex(
            model_name='memo',
            index=models.Index(fields=['dispatch_date'], name='memos_memo_dispatc_b22fab_idx'),
        ),
        migrations.AddIndex(
            model_name='memo',
            index=models.Index(fields=['due_date'], name='memos_memo_due_dat_e0185d_idx'),
        ),
        migrations.AddIndex(
            model_name='memo',
            index=models.Index(fields=['is_physical', 'department'], name='memos_memo_is_phys_f7d699_idx'),
        ),
    ]

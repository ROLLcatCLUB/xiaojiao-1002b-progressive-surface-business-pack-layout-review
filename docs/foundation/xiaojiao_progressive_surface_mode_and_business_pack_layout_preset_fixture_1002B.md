# 1002B Progressive Surface Mode and Business Pack Layout Preset Fixture

Stage:

`	ext
1002B_PROGRESSIVE_SURFACE_MODE_AND_BUSINESS_PACK_LAYOUT_PRESET_FIXTURE
`

Final status target:

`	ext
XIAOJIAO_PROGRESSIVE_SURFACE_MODE_AND_BUSINESS_PACK_LAYOUT_PRESET_FIXTURE_PASS
`

## Core Correction

Not every business pack should open a grid studio.

Business packs must first declare their recommended surface mode. Lightweight work should stay guided or focused. Complex teaching work can enter grid studio. Analysis work can enter analysis board. Classroom teaching can add teacher control and public display surfaces.

## Resource Library Judgment

The resource library is not a default studio. It is a support layer, search layer, reference layer, and recommendation layer.

It appears as:

`	ext
support_layer
resource_drawer
resource_picker
resource_cards_inside_other_workspaces
`

Only resource curation, classroom resource package creation, or teaching scene bundle assembly should open a resource grid studio.

## Required Business Packs

`	ext
teaching_plan_pack             -> guided_flow
lesson_design_pack             -> focus_surface
classroom_teaching_studio_pack -> grid_studio + teacher_control_surface + public_display_surface
student_evaluation_pack        -> analysis_board
resource_library_pack          -> support_layer + resource_drawer + resource_picker
resource_curation_pack         -> grid_studio
`

## Boundary

This stage is schema and fixture only. It does not install dependencies, modify real frontend files, connect runtime, call provider/model, write database or memory, write Feishu, create formal export, implement public display runtime, implement teacher control runtime, or implement production UI.
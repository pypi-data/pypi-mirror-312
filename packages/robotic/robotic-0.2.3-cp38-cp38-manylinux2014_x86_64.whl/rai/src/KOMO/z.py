    '''
         ------------------------------------------------------------------
        Copyright (c) 2011-2024 Marc Toussaint
        email: toussaint@tu-berlin.de

        This code is distributed under the MIT License.
        Please see <root-path>/LICENSE for details.
        -------------------------------------------------------------- 
        '''

    #include 'manipTools.h'

    #include '../Optim/NLP_Solver.h'
    #include '../Optim/NLP_Sampler.h'

    ManipulationModelling.ManipulationModelling( str& _info)
        : info(_info)

    ManipulationModelling.ManipulationModelling( std.shared_ptr<KOMO>& _self.komo)
        : self.komo(_self.komo)

    def setup_inverse_kinematics(self, C, homing_scale, accumulated_collisions, joint_limits, quaternion_norms):
        '''
        setup a 1 phase single step problem
        '''
        CHECK(not self.komo, 'self.komo already given or previously setup')
        self.komo = ry.KOMO(C, 1., 1, 0, accumulated_collisions)
        self.komo.addControlObjective([], 0, homing_scale)
        if accumulated_collisions:
            self.komo.addObjective([], ry.FS.accumulatedCollisions, [], ry.OT.eq, [1e0])

        if joint_limits:
            self.komo.addObjective([], ry.FS.jointLimits, [], ry.OT.ineq, [1e0])

        if quaternion_norms:
            self.komo.addQuaternionNorms()

    def setup_sequence(self, C, K, homing_scale, velocity_scale, accumulated_collisions, joint_limits, quaternion_norms):
        CHECK(not self.komo, 'self.komo already given or previously setup')
        self.komo = ry.KOMO(C, double(K), 1, 1, accumulated_collisions)
        self.komo.addControlObjective([], 0, homing_scale)
        self.komo.addControlObjective([], 1, velocity_scale)
        if accumulated_collisions:
            self.komo.addObjective([], ry.FS.accumulatedCollisions, [], ry.OT.eq, [1e0])

        if joint_limits:
            self.komo.addObjective([], ry.FS.jointLimits, [], ry.OT.ineq, [1e0])

        if quaternion_norms:
            self.komo.addQuaternionNorms()

    def setup_motion(self, C, K, steps_per_phase, homing_scale, acceleration_scale, accumulated_collisions, joint_limits, quaternion_norms):
        CHECK(not self.komo, 'self.komo already given or previously setup')
        self.komo = ry.KOMO(C, double(K), steps_per_phase, 2, accumulated_collisions)
        if homing_scale>0.) self.komo.addControlObjective([], 0, homing_scale:
        self.komo.addControlObjective([], 2, acceleration_scale)
        if accumulated_collisions:
            self.komo.addObjective([], ry.FS.accumulatedCollisions, [], ry.OT.eq, [1e0])

        if joint_limits:
            self.komo.addObjective([], ry.FS.jointLimits, [], ry.OT.ineq, [1e0])

        if quaternion_norms:
            self.komo.addQuaternionNorms()

        # zero vel at end
        self.komo.addObjective([double(K)], ry.FS.qItself, [], ry.OT.eq, [1e0], [], 1)

    def setup_pick_and_place_waypoints(self, C, gripper, obj, homing_scale, velocity_scale, accumulated_collisions, joint_limits, quaternion_norms):
        '''
        setup a 2 phase pick-and-place problem, a pick switch at time 1, a place switch at time 2
           the place mode switch at the final time two might seem obselete, self switch also implies the geometric constraints of placeOn
        '''
        CHECK(not self.komo, 'self.komo already given or previously setup')
        setup_sequence(C, 2, homing_scale, velocity_scale, accumulated_collisions, joint_limits, quaternion_norms)

        self.komo.addModeSwitch([1., -1.], rai.SY_stable, [gripper, obj], True)

    def setup_point_to_point_motion(self, C, q1, homing_scale, acceleration_scale, accumulated_collisions, joint_limits, quaternion_norms):
        '''
        setup a 1 phase fine-grained motion problem with 2nd order (acceleration) control costs
        '''
        CHECK(not self.komo, 'self.komo already given or previously setup')
        setup_motion(C, 1, 32, homing_scale, acceleration_scale, accumulated_collisions, joint_limits, quaternion_norms)

        if q1.N:
            self.komo.initWithWaypoints([q1], 1, True, .5, 0)
            self.komo.addObjective([1.], ry.FS.qItself, [], ry.OT.eq, [1e0], q1)

    def setup_point_to_point_rrt(self, C, q0, q1, explicitCollisionPairs):
        rrt = ry.rai.PathFinder()
        rrt.setProblem(C, q0, q1)
        if explicitCollisionPairs.N) rrt.setExplicitCollisionPairs(explicitCollisionPairs:

    def add_helper_frame(self, type, parent, name, initFrame, rel, markerSize):
        f = self.komo.addFrameDof(name, parent, type, True, initFrame, rel)
        if markerSize>0.:
            f.setShape(rai.ry.ST.marker, [.2])
            f.setColor([1., 0., 1.])

        if f.joint:
            f.joint.sampleSdv=1.
            f.joint.setRandom(self.komo.timeSlices.d1, 0)

    def grasp_top_box(self, time, gripper, obj, grasp_direction):
        '''
        grasp a box with a centered top grasp (axes fully aligned)
        '''
        rai.Array<FeatureSymbol> align
        if grasp_direction == 'xz':
            align = [ry.FS.scalarProductXY, ry.FS.scalarProductXZ, ry.FS.scalarProductYZ] 

        elif grasp_direction == 'yz':
            align = [ry.FS.scalarProductYY, ry.FS.scalarProductXZ, ry.FS.scalarProductYZ] 

        elif grasp_direction == 'xy':
            align = [ry.FS.scalarProductXY, ry.FS.scalarProductXZ, ry.FS.scalarProductZZ] 

        elif grasp_direction == 'zy':
            align = [ry.FS.scalarProductXX, ry.FS.scalarProductXZ, ry.FS.scalarProductZZ] 

        elif grasp_direction == 'yx':
            align = [ry.FS.scalarProductYY, ry.FS.scalarProductYZ, ry.FS.scalarProductZZ] 

        elif grasp_direction == 'zx':
            align = [ry.FS.scalarProductYX, ry.FS.scalarProductYZ, ry.FS.scalarProductZZ] 

        else:
            LOG(-2) <<'pickDirection not defined:' <<grasp_direction

        # position: centered
        self.komo.addObjective([time], ry.FS.positionDiff, [gripper, obj], ry.OT.eq, [1e1])

        # orientation: grasp axis orthoginal to target plane X-specific
        self.komo.addObjective([time-.2, time], align[0], [obj, gripper], ry.OT.eq, [1e0])
        self.komo.addObjective([time-.2, time], align[1], [obj, gripper], ry.OT.eq, [1e0])
        self.komo.addObjective([time-.2, time], align[2], [obj, gripper], ry.OT.eq, [1e0])

    def grasp_box(self, time, gripper, obj, palm, grasp_direction, margin):
        '''
        general grasp of a box, along provided grasp_axis (. 3
           possible grasps of a box), and angle of grasp is decided by
           inequalities on grasp plan and no-collision of box and palm
        '''
        arr xLine, yzPlane
        rai.Array<FeatureSymbol> align
        if grasp_direction == 'x':
            xLine = np.array([[1, 0, 0]]) 
            yzPlane = np.array([[2, 3}, {0, 1, 0, 0, 0, 1]]) 
            align = [ry.FS.scalarProductXY, ry.FS.scalarProductXZ] 

        elif grasp_direction == 'y':
            xLine = np.array([[0, 1, 0]]) 
            yzPlane = np.array([[2, 3}, {1, 0, 0, 0, 0, 1]]) 
            align = [ry.FS.scalarProductXX, ry.FS.scalarProductXZ] 

        elif grasp_direction == 'z':
            xLine = np.array([[0, 0, 1]]) 
            yzPlane = np.array([[2, 3}, {1, 0, 0, 0, 1, 0]]) 
            align = [ry.FS.scalarProductXX, ry.FS.scalarProductXY] 

        else:
            LOG(-2) <<'grasp_direction not defined:' <<grasp_direction

        boxSize = self.komo.world.getFrame(obj).getSize()
        boxSize.resizeCopy[3]

        # position: center in inner target plane X-specific
        self.komo.addObjective([time], ry.FS.positionRel, [gripper, obj], ry.OT.eq, xLine*1e1)
        self.komo.addObjective([time], ry.FS.positionRel, [gripper, obj], ry.OT.ineq, yzPlane*1e1, .5*boxSize-margin)
        self.komo.addObjective([time], ry.FS.positionRel, [gripper, obj], ry.OT.ineq, yzPlane*(-1e1), -.5*boxSize+margin)

        # orientation: grasp axis orthoginal to target plane X-specific
        self.komo.addObjective([time-.2, time], align[0], [gripper, obj], ry.OT.eq, [1e0])
        self.komo.addObjective([time-.2, time], align[1], [gripper, obj], ry.OT.eq, [1e0])

        # no collision with palm
        self.komo.addObjective([time-.3, time], ry.FS.distance, [palm, obj], ry.OT.ineq, [1e1], [-.001])

    def grasp_cylinder(self, time, gripper, obj, palm, margin):
        '''
        general grasp of a cylinder, squeezing the axis normally,
           inequality along z-axis for positioning, no-collision with palm
        '''
        size = self.komo.world.getFrame(obj).getSize()

        # position: center along axis, within z-range
        self.komo.addObjective([time], ry.FS.positionRel, [gripper, obj], ry.OT.eq, np.array([[2, 3}, {1, 0, 0, 0, 1, 0]])*1e1)
        self.komo.addObjective([time], ry.FS.positionRel, [gripper, obj], ry.OT.ineq, np.array([[0, 0, 1]])*1e1, np.array([[0., 0., .5*size[0]-margin]]))
        self.komo.addObjective([time], ry.FS.positionRel, [gripper, obj], ry.OT.ineq, np.array([[0, 0, 1]])*(-1e1), np.array([[0., 0., -.5*size[0]+margin]]))

        # orientation: grasp axis orthoginal to target plane X-specific
        self.komo.addObjective([time-.2, time], ry.FS.scalarProductXZ, [gripper, obj], ry.OT.eq, [1e0])

        # no collision with palm
        self.komo.addObjective([time-.3, time], ry.FS.distance, [palm, obj], ry.OT.ineq, [1e1], [-.001])

    #void ManipulationModelling.grasp_cylinder(double time, gripper, obj, palm, margin)#  size = self.komo.world[obj].getSize()

    #  self.komo.addObjective([time], ry.FS.positionRel, [gripper, obj], ry.OT.eq, arr([2,3],[1,0,0,0,1,0])*1e1)
    #  self.komo.addObjective([time], ry.FS.positionRel, [gripper, obj], ry.OT.ineq, arr([1,3],[0,0,1])*1e1, [0.,0.,.5*size[0]-margin])
    #  self.komo.addObjective([time], ry.FS.positionRel, [gripper, obj], ry.OT.ineq, arr([1,3],[0,0,1])*(-1e1), [0.,0.,-.5*size[0]+margin])

    #  # orientation: grasp axis orthoginal to target plane X-specific
    #  self.komo.addObjective([time-.2,time], ry.FS.scalarProductXZ, [gripper, obj], ry.OT.eq, [1e0])

    #  # no collision with palm
    #  self.komo.addObjective([time-.3,time], ry.FS.negDistance, [palm, obj], ry.OT.ineq, [1e1], [-.001])
    #

    #void ManipulationModelling.no_collision( arr& times, obj1, obj2, margin)#  self.komo.addObjective(times, ry.FS.negDistance, [obj1, obj2], ry.OT.ineq, [1e1], [-margin])
    #

    def place_box(self, time, obj, table, palm, place_direction, margin):
        '''
        placement of one box on another
        '''
        zVectorTarget = np.array([[0., 0., 1.]]) 
        rai.Frame *obj_frame = self.komo.world.getFrame(obj)
        boxSize = obj_frame.getSize()
        if obj_frame.shape.type()==rai.ry.ST.ssBox:
            boxSize.resizeCopy[3]

        elif obj_frame.shape.type()==rai.ry.ST.ssCylinder:
            boxSize = [boxSize[1], boxSize[1], boxSize[0]] 

        else NIY
            tableSize = self.komo.world.getFrame(table).getSize()
        tableSize.resizeCopy[3]
        double relPos=0.
        FeatureSymbol zVector
        rai.Array<FeatureSymbol> align
        if place_direction == 'x':
            relPos = .5*(boxSize[0]+tableSize[2])
            zVector = ry.FS.vectorX
            align = [ry.FS.scalarProductXX, ry.FS.scalarProductYX] 

        elif place_direction == 'y':
            relPos = .5*(boxSize[1]+tableSize[2])
            zVector = ry.FS.vectorY
            align = [ry.FS.scalarProductXY, ry.FS.scalarProductYY] 

        elif place_direction == 'z':
            relPos = .5*(boxSize[2]+tableSize[2])
            zVector = ry.FS.vectorZ
            align = [ry.FS.scalarProductXZ, ry.FS.scalarProductYZ] 

        elif place_direction == 'xNeg':
            relPos = .5*(boxSize[0]+tableSize[2])
            zVector = ry.FS.vectorX
            zVectorTarget *= -1.
            align = [ry.FS.scalarProductXX, ry.FS.scalarProductYX] 

        elif place_direction == 'yNeg':
            relPos = .5*(boxSize[1]+tableSize[2])
            zVector = ry.FS.vectorY
            zVectorTarget *= -1.
            align = [ry.FS.scalarProductXY, ry.FS.scalarProductYY] 

        elif place_direction == 'zNeg':
            relPos = .5*(boxSize[2]+tableSize[2])
            zVector = ry.FS.vectorZ
            zVectorTarget *= -1.
            align = [ry.FS.scalarProductXZ, ry.FS.scalarProductYZ] 

        else:
            LOG(-2) <<'place_direction not defined:' <<place_direction

        # position: above table, table
        self.komo.addObjective([time], ry.FS.positionDiff, [obj, table], ry.OT.eq, 1e1*np.array([[1, 3}, {0, 0, 1]]), np.array([[.0, .0, relPos]]))
        self.komo.addObjective([time], ry.FS.positionRel, [obj, table], ry.OT.ineq, 1e1*np.array([[2, 3}, {1, 0, 0, 0, 1, 0]]), .5*tableSize-margin)
        self.komo.addObjective([time], ry.FS.positionRel, [obj, table], ry.OT.ineq, -1e1*np.array([[2, 3}, {1, 0, 0, 0, 1, 0]]), -.5*tableSize+margin)

        # orientation: Z-up
        self.komo.addObjective([time-.2, time], zVector, [obj], ry.OT.eq, [0.5], zVectorTarget)
        self.komo.addObjective([time-.2, time], align[0], [table, obj], ry.OT.eq, [1e0])
        self.komo.addObjective([time-.2, time], align[1], [table, obj], ry.OT.eq, [1e0])

        # no collision with palm
        if palm) self.komo.addObjective([time-.3, time], ry.FS.distance, [palm, table], ry.OT.ineq, [1e1], [-.001]:

    def straight_push(self, time_interval, obj, gripper, table):
        #start & end helper frames
        helperStart = STRING('_straight_pushStart_' <<gripper <<'_' <<obj <<'_' <<time_interval[0])
        helperEnd = STRING('_straight_pushEnd_' <<gripper <<'_' <<obj <<'_' <<time_interval[1])
        if not self.komo.world.getFrame(helperStart, False):
            add_helper_frame(rai.JT_hingeZ, table, helperStart, obj, 0, .3)
        if not self.komo.world.getFrame(helperEnd, False):
            add_helper_frame(rai.JT_transXYPhi, table, helperEnd, obj, 0, .3)

        #-- couple both frames symmetricaly
        #aligned orientation
        self.komo.addObjective([time_interval[0]], ry.FS.vectorYDiff, [helperStart, helperEnd], ry.OT.eq, [1e1])
        #aligned position
        self.komo.addObjective([time_interval[0]], ry.FS.positionRel, [helperEnd, helperStart], ry.OT.eq, 1e1*np.array([[2, 3}, {1., 0., 0., 0., 0., 1.]]))
        self.komo.addObjective([time_interval[0]], ry.FS.positionRel, [helperStart, helperEnd], ry.OT.eq, 1e1*np.array([[2, 3}, {1., 0., 0., 0., 0., 1.]]))
        #at least 2cm appart, positivenot !not  direction
        self.komo.addObjective([time_interval[0]], ry.FS.positionRel, [helperEnd, helperStart], ry.OT.ineq, -1e2*np.array([[1, 3}, [0., 1., 0.]]), {.0, .02, .0])
        self.komo.addObjective([time_interval[0]], ry.FS.positionRel, [helperStart, helperEnd], ry.OT.ineq, 1e2*np.array([[1, 3}, [0., 1., 0.]]), {.0, -.02, .0])

        #gripper touch
        self.komo.addObjective([time_interval[0]], ry.FS.negDistance, [gripper, obj], ry.OT.eq, [1e1], [-.02])
        #gripper start position
        self.komo.addObjective([time_interval[0]], ry.FS.positionRel, [gripper, helperStart], ry.OT.eq, 1e1*np.array([[2, 3}, {1., 0., 0., 0., 0., 1.]]))
        self.komo.addObjective([time_interval[0]], ry.FS.positionRel, [gripper, helperStart], ry.OT.ineq, 1e1*np.array([[1, 3}, [0., 1., 0.]]), {.0, -.02, .0])
        #gripper start orientation
        self.komo.addObjective([time_interval[0]], ry.FS.scalarProductYY, [gripper, helperStart], ry.OT.ineq, [-1e1], [.2])
        self.komo.addObjective([time_interval[0]], ry.FS.scalarProductYZ, [gripper, helperStart], ry.OT.ineq, [-1e1], [.2])
        self.komo.addObjective([time_interval[0]], ry.FS.vectorXDiff, [gripper, helperStart], ry.OT.eq, [1e1])

        #obj end position
        self.komo.addObjective([time_interval[1]], ry.FS.positionDiff, [obj, helperEnd], ry.OT.eq, [1e1])
        #obj end orientation: unchanged
        self.komo.addObjective([time_interval[1]], ry.FS.quaternion, [obj], ry.OT.eq, [1e1], [], 1); #qobjPose.rot.getArr4d())

    def no_collision(self, time_interval, pairs, margin):
        '''
        inequality on distance between two objects
        '''
        _pairs = pairs.ref()
        _pairs.reshape(-1,2)
        for(uint i=0; i<_pairs.d0; i++)
            self.komo.addObjective(time_interval, ry.FS.negDistance, _pairs[i], ry.OT.ineq, [1e1], [-margin])

    def switch_pick(self):
        '''
        a kinematic mode switch, obj becomes attached to gripper, freely parameterized but stable (=constant) relative pose
        '''

    def switch_place(self):
        '''
        a kinematic mode switch, obj becomes attached to table, a 3D parameterized (XYPhi) stable relative pose
           self requires obj and table to be boxes and assumes default placement alone z-axis
           more general placements have to be modelled with switch_pick (table picking the object) and additinal user-defined geometric constraints
        '''

    def target_position(self):
        '''
        impose a specific 3D target position on some object
        '''

    def target_relative_xy_position(self, time, obj, relativeTo, pos):
        '''
        impose a specific 3D target position on some object
        '''
        if pos.N==2:
            pos.append(0.)

        self.komo.addObjective([time], ry.FS.positionRel, [obj, relativeTo], ry.OT.eq, 1e1*np.array([[2, 3}, {1, 0, 0, 0, 1, 0]]), pos)

    def target_x_orientation(self, time, obj, x_vector):
        self.komo.addObjective([time], ry.FS.vectorX, [obj], ry.OT.eq, [1e1], x_vector)

    def bias(self, time, qBias, scale):
        '''
        impose a square potential bias directly in joint space
        '''
        self.komo.addObjective([time], ry.FS.qItself, [], ry.OT.sos, [scale], qBias)

    def retract(self, time_interval, gripper, dist):
        helper = STRING('_' <<gripper <<'_retract_' <<time_interval[0])
        t = conv_time2step(time_interval[0], self.komo.stepsPerPhase)
        pose = self.komo.timeSlices(self.komo.k_order+t, self.komo.world[gripper].ID).getPose()
        add_helper_frame(rai.JT_none, 0, helper, 0, pose)
    #  self.komo.view(True, helper)

        self.komo.addObjective(time_interval, ry.FS.positionRel, [gripper, helper], ry.OT.eq, * np.array([[1, 3}, {1, 0, 0]]))
        self.komo.addObjective(time_interval, ry.FS.quaternionDiff, [gripper, helper], ry.OT.eq, [1e2])
        self.komo.addObjective([time_interval[1]], ry.FS.positionRel, [gripper, helper], ry.OT.ineq, -1e2 * np.array([[1, 3}, [0, 0, 1]]), {0., 0., dist])

    def approach(self, time_interval, gripper, dist):
        helper = STRING('_' <<gripper <<'_approach_' <<time_interval[1])
        t = conv_time2step(time_interval[1], self.komo.stepsPerPhase)
        pose = self.komo.timeSlices(self.komo.k_order+t, self.komo.world[gripper].ID).getPose()
        add_helper_frame(rai.JT_none, 0, helper, 0, pose)
    #  self.komo.view(True, helper)

        self.komo.addObjective(time_interval, ry.FS.positionRel, [gripper, helper], ry.OT.eq, * np.array([[1, 3}, {1, 0, 0]]))
        self.komo.addObjective(time_interval, ry.FS.quaternionDiff, [gripper, helper], ry.OT.eq, [1e2])
        self.komo.addObjective([time_interval[0]], ry.FS.positionRel, [gripper, helper], ry.OT.ineq, -1e2 * np.array([[1, 3}, [0, 0, 1]]), {0., 0., dist])

    def retractPush(self, time_interval, gripper, dist):
        helper = STRING('_' <<gripper <<'_retractPush_'  <<time_interval[0])
        t = conv_time2step(time_interval[0], self.komo.stepsPerPhase)
        pose = self.komo.timeSlices(self.komo.k_order+t, self.komo.world[gripper].ID).getPose()
        add_helper_frame(rai.JT_none, 0, helper, 0, pose)
    #  self.komo.addObjective(time_interval, ry.FS.positionRel, [gripper, helper], ry.OT.eq, * np.array([[1,3},{1,0,0]]))
    #  self.komo.addObjective(time_interval, ry.FS.quaternionDiff, [gripper, helper], ry.OT.eq, [1e2])
        self.komo.addObjective(time_interval, ry.FS.positionRel, [gripper, helper], ry.OT.eq, * np.array([[1, 3}, {1, 0, 0]]))
        self.komo.addObjective([time_interval[1]], ry.FS.positionRel, [gripper, helper], ry.OT.ineq, * np.array([[1, 3}, [0, 1, 0]]), {0., -dist, 0.])
        self.komo.addObjective([time_interval[1]], ry.FS.positionRel, [gripper, helper], ry.OT.ineq, -1e2 * np.array([[1, 3}, [0, 0, 1]]), {0., 0., dist])

    def approachPush(self, time_interval, gripper, dist, _helper):
    #  if not helper.N) helper = STRING('_push_start':
    #  self.komo.addObjective(time_interval, ry.FS.positionRel, [gripper, helper], ry.OT.eq, * np.array([[2,3},{1,0,0,0,0,1]]))
    #  self.komo.addObjective([time_interval[0]], ry.FS.positionRel, [gripper, helper], ry.OT.ineq, * np.array([[1,3},[0,1,0]]), {0., -dist, 0.])
        helper = STRING('_' <<gripper <<'_approachPush_' <<time_interval[1])
        t = conv_time2step(time_interval[1], self.komo.stepsPerPhase)
        pose = self.komo.timeSlices(self.komo.k_order+t, self.komo.world[gripper].ID).getPose()
        add_helper_frame(rai.JT_none, 0, helper, 0, pose)
        self.komo.addObjective(time_interval, ry.FS.positionRel, [gripper, helper], ry.OT.eq, * np.array([[1, 3}, {1, 0, 0]]))
        self.komo.addObjective([time_interval[0]], ry.FS.positionRel, [gripper, helper], ry.OT.ineq, * np.array([[1, 3}, [0, 1, 0]]), {0., -dist, 0.])
        self.komo.addObjective([time_interval[0]], ry.FS.positionRel, [gripper, helper], ry.OT.ineq, -1e2 * np.array([[1, 3}, [0, 0, 1]]), {0., 0., dist])

    def solve(self, verbose):
        if self.komo:
            NLP_Solver sol
            sol.setProblem(self.komo.nlp())
            sol.opt.set_damping(1e-1). set_verbose(verbose-1). set_stopTolerance(1e-3). set_maxLambda(100.). set_stopInners(20). set_stopEvals(200)
            ret = sol.solve()
            if ret.feasible:
                path = self.komo.getPath_qOrg()

            else:
                path.clear()

            if verbose>0:
                if not ret.feasible:
                    cout <<'  -- infeasible:' <<info <<'\n     ' <<*ret <<endl
                    if verbose>1:
                        cout <<sol.reportLagrangeGradients(self.komo.featureNames) <<endl
                        cout <<self.komo.report(False, True, verbose>1) <<endl
                        cout <<'  --' <<endl

                    self.komo.view(True, STRING('infeasible: ' <<info <<'\n' <<*ret))
                    if verbose>2:
                        while(self.komo.view_play(True, 0, 1.))

                else:
                    cout <<'  -- feasible:' <<info <<'\n     ' <<*ret <<endl
                    if verbose>2:
                        cout <<sol.reportLagrangeGradients(self.komo.featureNames) <<endl
                        cout <<self.komo.report(False, True, verbose>2) <<endl
                        cout <<'  --' <<endl
                        self.komo.view(True, STRING('feasible: ' <<info <<'\n' <<*ret))
                        if verbose>3:
                            while(self.komo.view_play(True, 0, 1.))

        elif rrt:
            rrt.rrtSolver.verbose=verbose
            ret = rrt.solve()
            if(ret.feasible) path = ret.x
            else path.clear()

        else:
            NIY

        return path

    def sample(self, sampleMethod, verbose):
        CHECK(self.komo, '')

        NLP_Sampler sol(self.komo.nlp())
        arr data
        uintA dataEvals
        time = -rai.cpuTime()

    #  sol.opt.seedMethod='gauss'
        if(sampleMethod) sol.opt.seedMethod=sampleMethod
        sol.opt.verbose=verbose
        sol.opt.downhillMaxSteps=50
        sol.opt.slackMaxStep=.5

        sol.run(data, dataEvals)
        time += rai.cpuTime()

        ret = ry.SolverReturn()
        if data.N:
            ret.x = data.reshape(-1)
            ret.evals = dataEvals.elem()
            ret.feasible = True

        else:
            ret.evals = self.komo.evalCount
            ret.feasible = False

        ret.time = time
        ret.done = True
            totals = self.komo.info_errorTotals(self.komo.info_objectiveErrorTraces())
            ret.sos = totals(ry.OT.sos)
            ret.ineq = totals(ry.OT.ineq)
            ret.eq = totals(ry.OT.eq)
            ret.f = totals(ry.OT.f)

        if ret.feasible:
            path = self.komo.getPath_qOrg()

        else:
            path.clear()

        if not ret.feasible:
            if verbose>0:
                cout <<'  -- infeasible:' <<info <<'\n     ' <<*ret <<endl
                if verbose>1:
                    cout <<self.komo.report(False, True, verbose>1) <<endl
                    cout <<'  --' <<endl

                self.komo.view(True, STRING('infeasible: ' <<info <<'\n' <<*ret))
                if verbose>2:
                    while(self.komo.view_play(True, 0, 1.))

        else:
            if verbose>0:
                cout <<'  -- feasible:' <<info <<'\n     ' <<*ret <<endl
                if verbose>2:
                    cout <<self.komo.report(False, True, verbose>2) <<endl
                    cout <<'  --' <<endl
                    self.komo.view(True, STRING('feasible: ' <<info <<'\n' <<*ret))
                    if verbose>3:
                        while(self.komo.view_play(True, 0, 1.))

        return path

    def debug(self, listObjectives, plotOverTime):
        cout <<'  -- DEBUG: ' <<info <<endl
        cout <<'  == solver return: ' <<*ret <<endl
        cout <<'  == all KOMO objectives with increasing errors:\n' <<self.komo.report(False, listObjectives, plotOverTime) <<endl
    #  cout <<'  == objectives sorted by error and Lagrange gradient:\n' <<sol.reportLagrangeGradients(self.komo.featureNames) <<endl
        cout <<'  == view objective errors over slices in gnuplot' <<endl
        cout <<'  == scroll through solution in display window using SHIFT-scroll' <<endl
        self.komo.view(True, STRING('debug: ' <<info <<'\n' <<*ret))

    def play(self, C, duration):
        dofIndices = C.getDofIDs()
        for(uint t=0; t<path.d0; t++)
            C.setFrameState(self.komo.getConfiguration_X(t))
            C.setJointState(self.komo.getConfiguration_dofs(t, dofIndices))
            C.view(False, STRING('step ' <<t <<'\n' <<info))
            rai.wait(duration/path.d0)

    def sub_motion(self, phase, fixEnd, homing_scale, acceleration_scale, accumulated_collisions, quaternion_norms):
        rai.Configuration C
        arr q0, q1
        self.komo.getSubProblem(phase, C, q0, q1)

        if not fixEnd) q1.clear(:

        std.shared_ptr<ManipulationModelling> manip = ry.ManipulationModelling(STRING('sub_motion'<<phase))
        manip.setup_point_to_point_motion(C, q0, q1, homing_scale, acceleration_scale, accumulated_collisions, quaternion_norms)
        return manip

    def sub_rrt(self, phase, explicitCollisionPairs):
        rai.Configuration C
        arr q0, q1
        self.komo.getSubProblem(phase, C, q0, q1)

        std.shared_ptr<ManipulationModelling> manip = ry.ManipulationModelling(STRING('sub_rrt'<<phase))
        manip.setup_point_to_point_rrt(C, q0, q1, explicitCollisionPairs)
        return manip

